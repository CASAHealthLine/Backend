from django.db import models

from accounts.models import Account

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=False, null=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    employment_date = models.DateField()
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
