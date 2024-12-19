from django.contrib import admin

from queues.models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'room', 'status_name', 'created_at', 'updated_at')
    search_fields = ('patient__full_name', 'room__displayname')
    list_filter = ('status', 'room__displayname')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('order',)
        return self.readonly_fields

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['order']
        return []
    
    def status_name(self, obj):
        return obj.get_status_display()
    
    status_name.short_description = 'Status'