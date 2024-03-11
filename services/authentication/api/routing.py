from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('authentication/ws/login/', consumers.LoginConsumer.as_asgi()),
]
