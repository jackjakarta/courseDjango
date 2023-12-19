from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


AuthUserModel = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=250, required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    @staticmethod
    def validate_email(email):
        return email

    @staticmethod
    def validate_password(password):
        return password

    def create(self, validated_data):
        AuthUserModel.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=make_password(validated_data["password"]),
        )

    # def list(self, validated_data):
    #     pass
