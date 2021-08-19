from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url('graphql/', consumers.WebsocketConsumer.as_asgi()),
]
