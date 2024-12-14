from django.contrib import admin

from queues.models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'room', 'status', 'created_at')
    search_fields = ('patient__full_name', 'room__displayname')
    
admin.site.unregister(Queue)
admin.site.register(Queue, QueueAdmin)