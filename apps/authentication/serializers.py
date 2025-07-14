from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['mobile', 'name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=10)
    purpose = serializers.ChoiceField(choices=[('login', 'Login'), ('reset', 'Reset')])

class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile', 'name', 'email']
