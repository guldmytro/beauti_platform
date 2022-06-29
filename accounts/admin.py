from django.contrib import admin
from .models import City, Profile


admin.site.register(City)
admin.site.register(Profile)


class CityAdmin(admin.ModelAdmin):
    list_display = ['osm_id']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname']