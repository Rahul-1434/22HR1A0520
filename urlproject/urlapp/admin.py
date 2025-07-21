from django.contrib import admin
from .models import Url, Detail

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'short_code', 'create_time', 'validity', 'clicks']
    search_fields = ['url', 'short_code']

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'short', 'click_time', 'referrer', 'location']
    search_fields = ['short__short_code', 'referrer', 'location']
