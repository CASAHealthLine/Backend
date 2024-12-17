from django.contrib import admin

from queues.models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'room', 'status_name', 'created_at', 'updated_at', 'order')
    search_fields = ('patient__full_name', 'room__displayname')
    list_filter = ('status', 'room__displayname')
    
    def status_name(self, obj):
        print(f"Status: {obj.status}, Display: {obj.get_status_display()}")
        return obj.get_status_display()
    
    status_name.short_description = 'Status'
    
