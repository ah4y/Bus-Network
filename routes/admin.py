from django.contrib import admin
from .models import Station, Route


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'duration')
    list_filter = ('origin', 'destination')
    filter_horizontal = ('passengers',)
