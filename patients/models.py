from django.db import models

from accounts.models import Account


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    verified = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    bhyt = models.CharField(max_length=20, blank=True, null=True)
    cccd = models.CharField(max_length=15)
    job = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name