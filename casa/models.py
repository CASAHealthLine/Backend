from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Model CustomUser (tùy chỉnh user)
class CustomUser(AbstractUser):
    phone = PhoneNumberField(unique=True, null=True, blank=False)  # Số điện thoại bắt buộc
    email = models.EmailField(unique=True)  # Email bắt buộc và duy nhất
    user_type = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),           # Người dùng
            ('doctor', 'Doctor'),       # Bác sĩ
            ('specialist', 'Specialist'),  # Chuyên viên
            ('receptionist', 'Receptionist'),  # Lễ tân
            ('admin', 'Admin')          # Quản trị viên
        ],
        default='user'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Các trường bắt buộc khi tạo tài khoản
    USERNAME_FIELD = 'username'  # Admin đăng nhập bằng username

    def __str__(self):
        if self.user_type == 'user':
            return str(self.phone)  # Trả về số điện thoại cho user
        return self.username  # Trả về username cho các loại tài khoản khác



# Model Note (ghi chú)
class Note(models.Model):
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Sử dụng model user tùy chỉnh
        on_delete=models.CASCADE,
        related_name='notes'
    )
