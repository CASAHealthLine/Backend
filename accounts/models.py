from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        (0, 'patient'),
        (1, 'doctor'),
        (2, 'admin'),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    type = models.IntegerField(choices=USER_TYPES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
