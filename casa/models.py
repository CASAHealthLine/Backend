from django.conf import settings  # Thêm import này
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Sử dụng model user tùy chỉnh
        on_delete=models.CASCADE,
        related_name='note'
    )

class CustomUser(AbstractUser):
    username = None  # Loại bỏ trường username
    phone = PhoneNumberField(unique=True, null=False, blank=False)  # Trường phone phải là duy nhất
    email = models.EmailField(unique=True)  # Đảm bảo email cũng là duy nhất (tùy chọn)
    USERNAME_FIELD = 'phone'  # Sử dụng phone để đăng nhập
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Các trường bắt buộc khi tạo user

    def __str__(self):
        return self.phone
