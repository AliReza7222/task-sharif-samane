import re

from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer[User]):
    password_confirmation = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
            "password",
            "password_confirmation",
        )

    def validate_phone_number(self, value):
        if not re.fullmatch(r"^09[0-9]{9}$", value):
            raise serializers.ValidationError(  # noqa: TRY003
                "Enter a valid phone number starting with 09.",  # noqa: EM101
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

        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
        )
