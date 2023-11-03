from django.contrib import admin
from .models import *
from mapbox_location_field.admin import MapAdmin

# Register your models here.
admin.site.register([Customer, Product, Service, OrderItem])
admin.site.register(Order, MapAdmin)
