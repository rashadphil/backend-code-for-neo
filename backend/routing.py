from django.urls import path

from chats import consumers

websocket_urlpatterns = [path("", consumers.ChatConsumer.as_asgi())]
