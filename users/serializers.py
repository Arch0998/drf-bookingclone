from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password must match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data.get("role", "guest"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
