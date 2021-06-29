from .models import User
from rest_framework import serializers


class RegisterFormSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    profile_image = serializers.ImageField(allow_null=True)
    is_active = serializers.BooleanField(allow_null=True, default=False)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "profile_image",
            "is_active"
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.profile_image = validated_data['profile_image']
        instance.token = validated_data['token']
        instance.is_active = True
        instance.save()
        return instance


class LoginFormSerializer(serializers.Serializer):
    print("user entered")
    username = serializers.CharField()
    password = serializers.CharField()


class UserBaseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
            'profile_image',
            'token',
        ]
