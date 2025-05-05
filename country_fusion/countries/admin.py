from django.contrib import admin
from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cca2', 'capital', 'region', 'population')
    list_filter = ('region', 'subregion')
    search_fields = ('name', 'cca2', 'cca3', 'capital')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'common_name', 'cca2', 'cca3', 'capital')
        }),
        ('Geographic Information', {
            'fields': ('region', 'subregion', 'population')
        }),
        ('Display Information', {
            'fields': ('flag_url', 'flag_emoji')
        }),
        ('Additional Information', {
            'fields': ('timezones', 'languages')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )