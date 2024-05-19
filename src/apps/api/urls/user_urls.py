from django.urls import path

from src.apps.api.views.user_views import UserCreateAPIView

urlpatterns = [
    path("", UserCreateAPIView.as_view()),
]
