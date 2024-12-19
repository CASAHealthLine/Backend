from django.contrib import admin
from .models import Room, RoomType

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'displayname', 'type', 'ip_address', 'created_at')
    list_filter = ('type',)
    search_fields = ('displayname', 'ip_address')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    search_fields = ('type_name',)
