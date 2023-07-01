"""
ASGI config for backend project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

from channels.routing import ProtocolTypeRouter, URLRouter
from configurations.asgi import get_asgi_application  # noqa

from . import routing

django_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": URLRouter(routing.websocket_urlpatterns),
    }
)
