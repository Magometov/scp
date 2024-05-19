from rest_framework.generics import CreateAPIView

from src.apps.users.api.serializers import UserCreateSerializer
from src.apps.users.models import User


class UserCreateAPIView(CreateAPIView[User]):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
