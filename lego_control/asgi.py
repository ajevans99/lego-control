"""
ASGI config for lego_control project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import channels
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from .routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lego_control.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": channels.routing.URLRouter(websocket_urlpatterns)
})
