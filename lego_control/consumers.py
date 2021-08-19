import channels_graphql_ws
from .schema import schema as graphql_schema

class WebsocketConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = graphql_schema

    confirm_subscriptions = True

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        print("New client connected!")
        print(f'Payload: {payload}')
        self.accept()
