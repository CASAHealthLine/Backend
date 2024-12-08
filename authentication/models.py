from django.db import models
import random
from django.utils.timezone import now
from datetime import timedelta

class ContactLink(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    tele_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telegram ID")
    email = models.EmailField(null=True, blank=True, verbose_name="Email Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Contact Link"
        verbose_name_plural = "Contact Links"

    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    try_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=now)

    @staticmethod
    def generate_otp(phone_number):
        otp = str(random.randint(1000, 9999))
        expires_at = now() + timedelta(minutes=5)
        otp_instance, created = OTP.objects.update_or_create(
            phone_number=phone_number,
            defaults={'otp': otp, 'expires_at': expires_at}
        )
        return otp