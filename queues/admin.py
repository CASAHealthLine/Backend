from django.contrib import admin

# Register your models here.
from .models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name', 'description')