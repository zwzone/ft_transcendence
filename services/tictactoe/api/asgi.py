import os

from .routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application
from .middleware import MyAuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": MyAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})


# """
# WSGI config for tictactoe project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# application = get_wsgi_application()
