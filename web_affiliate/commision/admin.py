from django.contrib import admin

# Register your models here.
from .models import Shop, Broker

admin.site.register(Shop)
admin.site.register(Broker)
