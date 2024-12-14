from django.contrib import admin
from .models import Account
    
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2', 'type')

class CustomUserChangeForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Nhập mật khẩu mới nếu muốn thay đổi. Để trống nếu không muốn thay đổi.",
    )

    class Meta:
        model = Account
        fields = ('username', 'display_name', 'email', 'is_active', 'is_staff', 'new_password', 'type')

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)  # Băm mật khẩu
        if commit:
            user.save()
        return user

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    readonly_fields = ('id', 'password', 'last_login')  # Chỉ đọc các trường này
    fieldsets = (
        (None, {'fields': ('username', 'display_name', 'email', 'new_password', 'type')}),  # Hiển thị trường nhập mật khẩu mới
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    list_display = ('id', 'username', 'display_name', 'email', 'type', 'is_active', 'is_staff')
    list_filter = ('type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'display_name')
    ordering = ('id',)

admin.site.unregister(Account)
admin.site.register(Account, AccountAdmin)