from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "last_login",
        "is_superuser",
        "is_staff",
    )
