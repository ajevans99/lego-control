import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import channels_graphql_ws
from .models import ControlPoint, ControlGroup, LightStrip


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class ControlPointNode(DjangoObjectType):
    class Meta:
        model = ControlPoint
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'online': ['exact'],
        }
        interfaces = (relay.Node, )


class ControlGroupNode(DjangoObjectType):
    class Meta:
        model = ControlGroup
        # Allow for some more advanced filtering here
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )


class LightStripNode(DjangoObjectType):
    class Meta:
        model = LightStrip
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'control_group__id': ['exact'],
        }
        interfaces = (relay.Node, )
    
    is_on = graphene.Boolean()

    def resolve_is_on(self, info):
        return self.is_on()


class Query(graphene.ObjectType):
    control_point = relay.Node.Field(ControlPointNode)
    all_control_points = DjangoFilterConnectionField(ControlPointNode)

    control_group = relay.Node.Field(ControlGroupNode)
    all_control_groups = DjangoFilterConnectionField(ControlGroupNode)

    light_strip = relay.Node.Field(LightStripNode)
    all_light_strips = DjangoFilterConnectionField(LightStripNode)


#### Mutations

class BrightnessMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.Int()
        brightness = graphene.Int()

    # The class attributes define the response of the mutation
    light_strip = graphene.Field(LightStripNode)

    @classmethod
    def mutate(cls, root, info, id, brightness):
        if brightness > 100 or brightness < 0:
            return ValueError(f'Brightness value should be between 0 and 100')
        light_strip = LightStrip.objects.get(id=id)
        light_strip.brightness = brightness
        light_strip.save()
        # Notice we return an instance of this mutation
        return BrightnessMutation(light_strip=light_strip)

class Mutation(graphene.ObjectType):
    brightness_mutation = BrightnessMutation.Field()

#### Subscriptions

class ControlPointHeartbeat(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    event = graphene.String()

    class Arguments:
        """That is how subscription arguments are defined."""
        id = graphene.Int()

    @staticmethod
    def subscribe(root, info, id):
        """Called when user subscribes."""
        
        print(f"SUBSCRIBED - arg1 {id}")

        control_point = ControlPoint.objects.get(id=id)
        light_strips = LightStrip.objects.filter(control_point=control_point)

        group_ids = set(map(lambda light_strip: str(light_strip.control_group.id), light_strips))
        # control_group = ControlGroup.objects.filter(light_strips=light_strips)
        print(group_ids)
        # Return the list of subscription group names.
        return list(group_ids)

    @staticmethod
    def unsubscribed(root, info, id):
        print(f"Unsubscribed {id}")

    @staticmethod
    def publish(payload, info, id):
        """Called to notify the client."""

        print("PUBLISHED")

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.

        return ControlPointHeartbeat(event="Something has happened!")


class LightStripBrightnessMonitor(channels_graphql_ws.Subscription):
    # Subscription payload.
    brightness = graphene.Int()
    control_point_id = graphene.Int()
    previous_brightness = graphene.Int()
    gpio_control_pin = graphene.Int()

    class Arguments:
        """That is how subscription arguments are defined."""
        id = graphene.Int()

    @staticmethod
    def subscribe(root, info, id):
        """Called when user subscribes."""
        
        print(f"SUBSCRIBED - {id}")

        return [str(id)]

    @staticmethod
    def unsubscribed(root, info, id):
        print(f"Unsubscribed {id}")

    @staticmethod
    def publish(payload, info, id):
        """Called to notify the client."""

        print("PUBLISHED")

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.

        return LightStripBrightnessMonitor(
            brightness=payload['brightness'],
            control_point_id=payload['control_point_id'],
            previous_brightness=payload['previous_brightness'],
            gpio_control_pin=payload['gpio_control_pin'],
        )


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    control_point_heartbeat = ControlPointHeartbeat.Field()
    light_strip_brightness_monitor = LightStripBrightnessMonitor.Field()
