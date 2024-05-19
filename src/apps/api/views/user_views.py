from rest_framework.generics import CreateAPIView

from src.apps.users.models import User
from src.apps.users.serializers import UserCreateSerializer


class UserCreateAPIView(CreateAPIView[User]):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
