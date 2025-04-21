# asgi.py
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import AgentConsumer  # Import your WebSocket consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_rep.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/agent/", AgentConsumer.as_asgi()),  # WebSocket URL
        ])
    ),
})
