from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['phone_number', 'username', 'email', 'is_staff',
                    'is_active', 'is_verified']  # فیلدهایی که می‌خواهید در لیست نمایش دهید
    list_filter = ['is_staff', 'is_active', 'is_verified', 'user_type']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_verified', 'user_type')}),  # اضافه کردن فیلد شماره تلفن به فرم ویرایش
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'is_verified', 'user_type')}),  # اضافه کردن فیلد شماره تلفن به فرم افزودن کاربر
    )
    search_fields = ['phone_number', 'username', 'email', 'user_type']  # امکان جستجو بر اساس شماره تلفن


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)

