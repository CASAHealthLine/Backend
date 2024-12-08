from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'display_name', 'email', 'type', 'is_active', 'is_staff')
    list_filter = ('type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'display_name')
    ordering = ('id',)