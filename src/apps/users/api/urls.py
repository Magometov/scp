from django.urls import path

from src.apps.users.api.views import UserCreateAPIView

urlpatterns = [
    path("", UserCreateAPIView.as_view()),
]
