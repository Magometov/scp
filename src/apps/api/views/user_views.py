from django.db.models import Manager, QuerySet
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import BaseSerializer

from src.apps.users.models import User
from src.apps.users.serializers import UserCreateSerializer


class UserCreateAPIView(CreateAPIView[User]):
    queryset: QuerySet[User] | Manager[User] | None = User.objects.all()
    serializer_class: type[BaseSerializer[User]] = UserCreateSerializer
