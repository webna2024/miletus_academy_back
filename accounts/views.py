import json
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
import random
from .models import *
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login


def send_sms(phone_number, otp_code):
    """Send OTP SMS to the user's phone number."""
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS"
    payload = json.dumps({
        "sendDate": "2024-07-04T07:41:15.992Z",
        "receptors": [
            {
                "mobile": str(phone_number),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "Ghasedak",
        "inputs": [
            {
                "param": "Code",
                "value": str(otp_code)
            }
        ],
        "udh": True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': '8d5defd85aa08cf909734060cb95d58a2d4f8387780e80936f9e73134381a655D7JupkdXuCPojMoR'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()

            # Delete expired OTPs
            OTP.objects.filter(expires_at__lt=timezone.now()).delete()
            # create token
            otp_codes = OTP.objects.values_list('code', flat=True)
            while True:
                otp_code = random.randint(1000, 9999)
                if otp_code not in otp_codes:
                    break

            OTP.objects.create(user=user, code=otp_code)
            # Send SMS
            send_sms(user.phone_number, otp_code)
            data = {
                'detail': f'کد تایید برای شماره  {str(user.phone_number)} ارسال شد',
                'phone_number': str(user.phone_number)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpApiView(APIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        data = {
            'phone_number': request.data.get('phone_number')
        }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                obj = OTP.objects.get(code=otp_code, user__phone_number=request.data.get('phone_number'))
                # Check expiration
                if timezone.now() > obj.expires_at:
                    obj.delete()
                    data['detail'] = "کد  منقضی شده است."
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                if request.resolver_match.url_name == 'verify_registration':
                    user = obj.user
                    user.is_verified = True
                    user.save()
                    obj.delete()  # Delete OTP after verification
                    # Login and generate token
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"detail": "تایید موفقیت‌آمیز بود.", "token": token.key}, status=status.HTTP_200_OK)

                elif request.resolver_match.url_name == 'verify_forgot_password':
                    data['detail'] = 'تایید موفق امیز بود'
                    obj.delete()  # Delete OTP after verification
                    return Response(data, status=status.HTTP_200_OK)


            except:
                data['detail'] = 'کد نا معتبر است'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data['detail'] = 'کد نا معتبر است'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPApiView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if OTP.objects.filter(user=user).exists():
                OTP.objects.filter(user=user).delete()
            otp_codes = OTP.objects.values_list('code', flat=True)

            # create otp code
            while True:
                otp_code = random.randint(1000, 9999)
                if otp_code not in otp_codes:
                    break
            OTP.objects.create(user=user, code=otp_code)

            # send SMS
            send_sms(user.phone_number, otp_code)
            data = {
                'detail': 'کد تایید برای شما ارسال شد',
                'phone_number': phone_number
            }
            return Response(data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"detail": "کاربر با این شماره تلفن وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        print(user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["رمز عبور فعلی اشتباه است"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'detail': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(phone_number=serializer.validated_data['phone_number']).first()
        if user:
            if not user.is_verified:
                return Response({"error": "حساب کاربری شما تایید نشده است"}, status=400)
            # Delete expired OTPs
            OTP.objects.filter(expires_at__lt=timezone.now()).delete()
            # create token
            otp_codes = OTP.objects.values_list('code', flat=True)
            while True:
                otp_code = random.randint(1000, 9999)
                if otp_code not in otp_codes:
                    break

            OTP.objects.create(user=user, code=otp_code)
            # Send SMS
            send_sms(user.phone_number, otp_code)
            data = {
                'detail': f'کد تایید برای شماره  {str(user.phone_number)} ارسال شد',
                'phone_number': str(user.phone_number)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "کاربری با اطلاعات وارد شده یافت نشد"}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordSetApiView(generics.GenericAPIView):
    serializer_class = SetForgotPasswordSerializer

    def put(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(phone_number=phone_number)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'detail': 'رمز عیور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
