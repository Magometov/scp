from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from src.apps.notifications.services.email_confirmation import send_confirmation_email
from src.apps.users.api.serializers import UserCreateSerializer
from src.apps.users.const import VerificationResponse, VerificationStatusCodes
from src.apps.users.models import User
from src.apps.users.services.verification import (
    activate_user_by_token,
    verify_email_token,
)


class UserCreateAPIView(CreateAPIView[User]):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer: BaseSerializer[User]) -> None:
        user = serializer.save(is_active=False)
        send_confirmation_email(user)


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_user(request: Request) -> Response:
    verification_response: VerificationResponse = VerificationResponse.MISSING_TOKEN
    if token := request.query_params.get("token"):
        verification_response = verify_email_token(token)
        if verification_response is VerificationResponse.SUCCESS:
            activate_user_by_token(token)

    status_code = VerificationStatusCodes[verification_response]
    return Response(verification_response, status=status_code)
