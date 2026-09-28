# Django imports
from django.urls import re_path

# Project imports
from apps.chat.consumers import AdminChatConsumer, PublicChatConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/chat/admin/',
        AdminChatConsumer.as_asgi(),
    ),
    re_path(
        r'ws/chat/public/',
        PublicChatConsumer.as_asgi()
    ),
]
