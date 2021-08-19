from django.db import models
from django.db.models.signals import post_save, post_init

# Create your models here.

class ControlPoint(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    online = models.BooleanField(default=False)
    last_checkin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ControlGroup(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def is_synced(self):
        lights = LightStrip.objects.filter(control_group=self)
        if len(lights) == 0:
            return True
        return all(lights[0].brightness == light for light in lights[1:])


class LightStrip(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    brightness = models.IntegerField(default=100)
    previous_brightness = None
    gpio_control_pin = models.IntegerField(null=True, blank=True)
    control_point = models.ForeignKey(ControlPoint, on_delete=models.CASCADE)
    control_group = models.ForeignKey(ControlGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_on(self):
        return self.brightness > 0

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        print("post save")
        if instance.previous_brightness != instance.brightness or created:
            from . import schema

            schema.LightStripBrightnessMonitor.broadcast(
                # Subscription group to notify clients in.
                group = str(instance.id),
                # Dict delivered to the `publish` method.
                payload = {
                    'control_point_id': instance.control_point.id,
                    'brightness': instance.brightness,
                    'gpio_control_pin': instance.gpio_control_pin,
                    'previous_brightness': instance.previous_brightness,
                },
            )

    @staticmethod
    def remember_brightness(sender, **kwargs):
        instance = kwargs.get('instance')
        instance.previous_brightness = instance.brightness

post_save.connect(LightStrip.post_save, sender=LightStrip)
post_init.connect(LightStrip.remember_brightness, sender=LightStrip)
