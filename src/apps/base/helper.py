from typing import TYPE_CHECKING

from django.contrib import messages

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest


def sending_messages_in_admin_panel(self: "Any", request: "HttpRequest", message: str, level: int) -> None:
    self.message_user(request=request, message=message, level=level)
    messages.set_level(request, level)
