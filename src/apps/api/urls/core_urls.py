from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("users/", include("src.apps.api.urls.user_urls")),
]
