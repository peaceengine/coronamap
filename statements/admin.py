from django.contrib import admin

from .models import Statement, UserGeoLocation
# Register your models here.

admin.site.register(Statement)
admin.site.register(UserGeoLocation)