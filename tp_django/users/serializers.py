from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     new_password = serializers.CharField(write_only=True)
#     new_password2 = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         if attrs['new_password'] != attrs['new_password2']:
#             raise serializers.ValidationError("Les mots de passe ne correspondent pas")
#         validate_password(attrs['new_password'])
#         return attrs
