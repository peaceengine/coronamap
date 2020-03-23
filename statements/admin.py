from django.contrib import admin

from .models import Statement, Hashtag, Response, UserGeoLocation#, Response
# Register your models here.

admin.site.register(Statement)
admin.site.register(Response)
admin.site.register(UserGeoLocation)
admin.site.register(Hashtag)
# #admin.site.register(Response)
# admin.site.register(Choice)