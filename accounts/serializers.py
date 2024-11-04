from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username', 'password', 'password1']

    def validate(self, attrs):
        # validate phone number
        phone_number = attrs.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise serializers.ValidationError({'phone_number': 'شماره تلفن باید ۱۱ رقمی و فقط شامل اعداد باشد.'})

        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': 'رمز عبورها یکسان نیستند'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return CustomUser.objects.create_user(**validated_data)


class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=4)


class CustomAuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=_("phone_number"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('phone_number')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                # Unable to log in with provided credentials.
                msg = _('شماره تلفن یا رمز عبور اشتباه است')
                raise serializers.ValidationError(msg, code='authorization')

            # بررسی تایید شماره تلفن کاربر
            if not user.is_verified:
                raise serializers.ValidationError({
                    'detail': "این حساب کاربری هنوز تأیید نشده است",
                    'phone_number': user.phone_number
                }, code='authorization')

        else:
            # Must include "username" and "password".
            msg = _('وارد کردن شماره تلفن و رمز عبور الزامی است')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):

        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({'detail': 'رمزهای عبور با هم تطابق ندارند'})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, write_only=True)

    def validate(self, attrs):
        # validate phone number
        phone_number = attrs.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise serializers.ValidationError({'phone_number': 'شماره تلفن باید ۱۱ رقمی و فقط شامل اعداد باشد.'})
        return super().validate(attrs)


class SetForgotPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):

        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({'detail': 'رمزهای عبور با هم تطابق ندارند'})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)