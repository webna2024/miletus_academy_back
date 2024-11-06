from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.SmallIntegerField(default=0)  # 0 = student, 1 = teacher,2=admin
    USERNAME_FIELD = 'phone_number'
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


def get_expiration_time():
    return timezone.now() + timedelta(minutes=2)


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return self.user.phone_number
