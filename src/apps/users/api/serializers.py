from typing import Any

from django_stubs_ext.db.models import TypedModelMeta
from rest_framework import serializers

from src.apps.users.models import User


class UserCreateSerializer(serializers.ModelSerializer[User]):
    repeat_of_password = serializers.CharField(max_length=128, write_only=True)

    class Meta(TypedModelMeta):
        model = User
        fields = ["username", "email", "password", "repeat_of_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: Any) -> Any:
        if attrs["password"] != attrs.pop("repeat_of_password"):
            raise serializers.ValidationError({"repeat_of_password": "Password mismatch"})
        return attrs

    def create(self, validated_data: Any) -> User:
        return User.objects.create_user(**validated_data)
