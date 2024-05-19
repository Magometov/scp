from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.users.api.serializers import UserCreateSerializer
from src.apps.users.const import VerificationResponse, VerificationStatusCodes
from src.apps.users.models import User
from src.apps.users.services.verification import verify_email_token


class UserCreateAPIView(CreateAPIView[User]):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_user(request: Request) -> Response:
    verification_response: VerificationResponse = VerificationResponse.MISSING_TOKEN
    if token := request.query_params.get("token"):
        verification_response = verify_email_token(token)

    status_code = VerificationStatusCodes[verification_response]
    return Response(verification_response, status=status_code)
