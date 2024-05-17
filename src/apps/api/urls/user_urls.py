from django.urls import path

from src.apps.api.views.user_views import UserCreateAPIView

urlpatterns = [
    path("create/", UserCreateAPIView.as_view()),
]
