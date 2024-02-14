import os

from .routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from .middleware import MyAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            MyAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)