from rest_framework import serializers
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    display_name = serializers.CharField(max_length=50)

    class Meta:
        model = Account
        fields = ('username', 'password', 'display_name', 'type')

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            display_name=validated_data['display_name'],
            type=validated_data.get('type', 0)
        )
        return user
