from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_verified"]


class VerifyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "otp"]

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
