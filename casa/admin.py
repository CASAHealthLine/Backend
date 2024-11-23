from django.contrib import admin
from .models import Note, CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Note)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'phone', 'email', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'user_type', 'is_staff'),
        }),
    )
    search_fields = ['username', 'phone', 'email']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
