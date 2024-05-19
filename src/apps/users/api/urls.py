from django.urls import path

from src.apps.users.api.views import UserCreateAPIView, verify_user

app_name = "users"
urlpatterns = [
    path("", UserCreateAPIView.as_view(), name="sign-up"),
    path("verify/", verify_user, name="verify-user"),
]
