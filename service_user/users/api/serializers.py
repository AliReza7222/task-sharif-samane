import re

from rest_framework import serializers

from users.user import User


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirmation = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if User.get_user_by_email(value):
            raise serializers.ValidationError(
                "This email is already registered.",
            )
        return value

    def validate_phone_number(self, value):
        if not re.fullmatch(r"^09[0-9]{9}$", value):
            raise serializers.ValidationError(
                "Enter a valid phone number starting with 09.",
            )
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."},
            )
        return data

    def create(self, validated_data):
        del validated_data["password_confirmation"]
        user_id = User.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return {"id": user_id, **validated_data}


class UserRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
