# Python modules
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Django modules
from django.core.asgi import get_asgi_application

from apps.chat.routing import websocket_urlpatterns

# Project modules
from stack_underflow.conf import ENV_ID, ENV_POSSIBLE_OPTIONS

assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Invalid env id. Possible options {ENV_POSSIBLE_OPTIONS}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"stack_underflow.env.{ENV_ID}")

asgi = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": asgi,
        "websocket":  # AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
        # )
    }
)
