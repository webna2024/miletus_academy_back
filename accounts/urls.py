from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
    path('registration/verify/', views.VerifyOtpApiView.as_view(), name='verify_registration'),
    path('resend/otp/', views.ResendOTPApiView.as_view(), name='resend_otp'),
    path('login/token/', views.CustomAuthToken.as_view(), name='login_token'),
    path('logout/token/', views.CustomDiscardAuthToken.as_view(), name='logout_token'),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('forgot-password/', views.ForgotPasswordApiView.as_view(), name='forgot-password'),
    path('forgot-password/verify/', views.VerifyOtpApiView.as_view(), name='verify_forgot_password'),
    path('forgot-password/set/', views.ForgotPasswordSetApiView.as_view(), name='forgot_password_set'),

]
