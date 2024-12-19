from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .serializer import QueueSerializer
from .models import Queue
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()

@receiver(post_save, sender=Queue)
def queue_updated(sender, instance, created, **kwargs):
    instance.refresh_from_db()
    
    async_to_sync(channel_layer.group_send)(
        f'room_doctor_{instance.room.id}',
        {
            "type": "queue_update",
            "message": {
                "data": QueueSerializer(instance).data,
                "action": "created" if created else "updated",
            }
        },
    )
    
    current_queue = Queue.objects.filter(room=instance.room, status=0).first()
    next_queue = Queue.objects.filter(room=instance.room, status=1).first()
    
    my_queue = Queue.objects.filter(room=instance.room, patient=instance.patient, status__in=[0, 1]).first()
    async_to_sync(channel_layer.group_send)(
        f'patient_{instance.patient.id}',
        {
            "type": "queue_update",
            "message": {
                "current_number": current_queue.order if current_queue else None,
                "next_number": next_queue.order if next_queue else None,
                "my_number": my_queue.order if my_queue else None,
                "room_id": instance.room.id,
                "room_name": instance.room.displayname,
                "status": instance.status,
                "action": "deleted" if not instance.status in [0, 1] else "updated",
            },
        },
    )
    
    async_to_sync(channel_layer.group_send)(
        f'room_patient_{instance.room.id}',
        {
            "type": "queue_update",
            "message": {
                "current_number": current_queue.order if current_queue else None,
                "next_number": next_queue.order if next_queue else None,
                "room_id": instance.room.id,
            },
        },
    )

@receiver(post_delete, sender=Queue)
def queue_deleted(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        f'room_doctor_{instance.room.id}',
        {
            "type": "queue_update",
            "message": {
                "id": instance.id,
                "action": "deleted",
            },
        },
    )