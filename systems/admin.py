from django.contrib import admin
from .models import ControlPoint, ControlGroup, LightStrip

# Register your models here.
@admin.register(ControlPoint, ControlGroup, LightStrip)
class LegoControlAdmin(admin.ModelAdmin):
    pass
