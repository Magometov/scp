from typing import Any

from django_stubs_ext.db.models import TypedModelMeta
from rest_framework import serializers

from src.apps.users.models import User


class UserCreateSerializer(serializers.ModelSerializer[User]):
    repeat_of_password: "serializers.CharField" = serializers.CharField(max_length=128, write_only=True)

    class Meta(TypedModelMeta):
        model = User
        fields = ["username", "email", "password", "repeat_of_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: Any) -> Any:
        if attrs["password"] != attrs["repeat_of_password"]:
            raise serializers.ValidationError("Passwords are not equal!")
        return attrs

    def create(self, validated_data: Any) -> User:
        del validated_data["repeat_of_password"]
        user: User = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
