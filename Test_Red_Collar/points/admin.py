from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Comment

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('name', 'created_at') 
    list_display_links = ('name',)
    list_filter = ('created_at',)
    search_fields = ('name',)
    settings_overrides = {
        'DEFAULT_CENTER': (55.7558, 37.6173),
        'DEFAULT_ZOOM': 10,
    }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'location', 'created_at')
