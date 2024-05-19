from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api_auth"
urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="obtain-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-pair"),
]
