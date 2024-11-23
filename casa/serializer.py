from rest_framework import serializers
from .models import Note, CustomUser

# Serializer cho đăng ký tài khoản user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            user_type='user'  # Đăng ký chỉ tạo tài khoản loại user
        )
        user.set_password(validated_data['password'])  # Mã hóa mật khẩu
        user.save()
        return user

# Serializer cho việc hiển thị thông tin người dùng
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


# Serializer cho model Note
class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Hiển thị thông tin owner dưới dạng string (username)

    class Meta:
        model = Note
        fields = ['id', 'description']

# Admin vẫn có thể quản lý các tài khoản doctor, specialist, và receptionist, với username bắt buộc:
class AdminCreateStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
