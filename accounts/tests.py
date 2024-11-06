from .views import *
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, OTP
from rest_framework.test import APITestCase
from unittest.mock import patch
from rest_framework.authtoken.models import Token


# test url
class TestUrl(SimpleTestCase):
    def test_accounts_registration_url_resolves(self):
        url = reverse('accounts:registration')
        self.assertEqual(resolve(url).func.view_class, RegistrationApiView)

    def test_accounts_verify_registration_url_resolves(self):
        url = reverse('accounts:verify_registration')
        self.assertEqual(resolve(url).func.view_class, VerifyOtpApiView)

    def test_accounts_resend_otp_url_resolves(self):
        url = reverse('accounts:resend_otp')
        self.assertEqual(resolve(url).func.view_class, ResendOTPApiView)

    def test_accounts_login_token_url_resolves(self):
        url = reverse('accounts:login_token')
        self.assertEqual(resolve(url).func.view_class, CustomAuthToken)

    def test_accounts_logout_token_url_resolves(self):
        url = reverse('accounts:logout_token')
        self.assertEqual(resolve(url).func.view_class, CustomDiscardAuthToken)

    def test_accounts_change_password_url_resolves(self):
        url = reverse('accounts:change-password')
        self.assertEqual(resolve(url).func.view_class, ChangePasswordApiView)

    def test_accounts_forgot_password_url_resolves(self):
        url = reverse('accounts:forgot-password')
        self.assertEqual(resolve(url).func.view_class, ForgotPasswordApiView)

    def test_accounts_verify_forgot_password_url_resolves(self):
        url = reverse('accounts:verify_forgot_password')
        self.assertEqual(resolve(url).func.view_class, VerifyOtpApiView)

    def test_accounts_forgot_password_set_url_resolves(self):
        url = reverse('accounts:forgot_password_set')
        self.assertEqual(resolve(url).func.view_class, ForgotPasswordSetApiView)


# test model
class CustomUserModelTest(TestCase):
    def setUp(self):
        # ایجاد کاربر نمونه برای تست‌ها
        self.user = CustomUser.objects.create_user(
            phone_number="09123456789",
            username="testuser",
            password="testpassword123"
        )

    def test_create_user(self):
        # بررسی اینکه کاربر با شماره تلفن ایجاد شده است
        self.assertEqual(self.user.phone_number, "09123456789")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword123"))
        self.assertEqual(self.user.user_type, 0)

    def test_create_duplicate_user(self):
        # تلاش برای ایجاد یک کاربر با شماره تلفن تکراری
        with self.assertRaises(Exception) as raised_exception:
            duplicate_user = CustomUser.objects.create_user(
                phone_number="09123456789",
                username="testuser",
                password="duplicatepassword"
            )
        # بررسی اینکه خطای تکراری بودن به درستی رخ می‌دهد
        self.assertIn("duplicate key value violates unique constraint", str(raised_exception.exception))


class OTPModelTest(TestCase):
    def setUp(self):
        # ایجاد کاربر برای استفاده در تست‌های OTP
        self.user = CustomUser.objects.create_user(
            phone_number="09123456789",
            username="testuser",
            password="testpassword123"
        )

    def test_create_otp(self):
        # بررسی ایجاد کد OTP و تنظیم تاریخ انقضا
        otp = OTP.objects.create(user=self.user, code="1234")
        self.assertEqual(otp.user, self.user)
        self.assertEqual(otp.code, "1234")

        # بررسی زمان انقضا
        expected_expiration = timezone.now() + timedelta(minutes=2)
        self.assertAlmostEqual(otp.expires_at, expected_expiration, delta=timedelta(seconds=5))


# view test


class RegistrationApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:registration')  # مطمئن شوید که نام مسیر view صحیح باشد
        self.valid_data = {
            'phone_number': '09123456789',
            'username': 'testuser',
            'password': 'Testpassword123',
            'password1': 'Testpassword123',
        }
        self.invalid_data = {
            'phone_number': '09123456789',
            'username': 'testuser',
            # بدون پسورد برای ایجاد خطا
        }

    @patch('accounts.views.send_sms')
    def test_registration_with_valid_data(self, mock_send_sms):
        # تست ثبت نام با اطلاعات معتبر
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # بررسی ایجاد کاربر
        self.assertTrue(CustomUser.objects.filter(phone_number=self.valid_data['phone_number']).exists())

        # بررسی ایجاد OTP
        user = CustomUser.objects.get(phone_number=self.valid_data['phone_number'])
        otp = OTP.objects.filter(user=user).first()
        self.assertIsNotNone(otp)
        self.assertEqual(len(otp.code), 4)  # بررسی اینکه کد OTP چهار رقمی است

    def test_registration_with_invalid_data(self):
        # تست ثبت نام با اطلاعات نامعتبر
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)  # بررسی خطای پسورد


class CustomAuthTokenTests(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:login_token')  # اطمینان حاصل کنید که نام URL صحیح است
        self.user = CustomUser.objects.create_user(
            phone_number='09123456789',
            username='testuser',
            password='Testpassword123',
            is_verified=True
        )
        self.valid_credentials = {
            'phone_number': '09123456789',
            'password': 'Testpassword123'
        }
        self.invalid_credentials = {
            'phone_number': '09123456789',
            'password': 'wrongpassword'
        }

    def test_obtain_token_with_valid_credentials(self):
        # ارسال درخواست برای دریافت توکن با داده‌های معتبر
        response = self.client.post(self.url, self.valid_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # بررسی اینکه توکن در پاسخ وجود دارد
        self.assertIn('token', response.data)

        # بررسی اینکه توکن برای کاربر درست است
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

    def test_obtain_token_with_invalid_credentials(self):
        # ارسال درخواست برای دریافت توکن با داده‌های نامعتبر
        response = self.client.post(self.url, self.invalid_credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # بررسی اینکه توکن در پاسخ وجود ندارد
        self.assertNotIn('token', response.data)


class CustomDiscardAuthTokenTests(APITestCase):
    def setUp(self):
        # ایجاد یک کاربر و توکن برای او
        self.user = CustomUser.objects.create_user(
            phone_number="09112223344",
            username="testuser",
            password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('accounts:logout_token')

    def test_discard_token(self):
        # احراز هویت کاربر با توکن
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # ارسال درخواست POST برای حذف توکن
        response = self.client.post(self.url)

        # بررسی اینکه پاسخ با وضعیت 204 است
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # بررسی اینکه توکن حذف شده است
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_discard_token_unauthenticated(self):
        # ارسال درخواست POST بدون احراز هویت
        response = self.client.post(self.url)

        # بررسی اینکه پاسخ با وضعیت 401 Unauthorized است
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



