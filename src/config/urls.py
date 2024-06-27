from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        f"{settings.API_PREFIX}/tokens/",
        include("src.apps.api_auth.api.urls", namespace="api-auth"),
    ),
    path(
        f"{settings.API_PREFIX}/users/",
        include("src.apps.users.api.urls", namespace="users"),
    ),
]
