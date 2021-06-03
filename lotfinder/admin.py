#from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from .models import parkinglot,locality


# Register your models here.

#admin.site.register(parkinglot)
#admin.site.register(locality)

@register(locality)
class localityAdmin(ModelAdmin):
    icon_name = 'add_location'

@register(parkinglot)
class parkinglotAdmin(ModelAdmin):
    icon_name = 'local_car_wash'