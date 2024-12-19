from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
import time
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from accounts.models import Account
from patients.models import Patient
from queues.filters import QueueFilter
from queues.models import Queue

class QueueConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        from rooms.models import Room
        from .models import Queue
        
        self.group_name = "general"
        self.filters = {}
        self.user = self.scope['user']
        print(f"User: {self.user}")
        if self.user.is_authenticated:
            query_string = parse_qs(self.scope["query_string"].decode())
            
            ip_address = query_string.get("virtual_ip", [None])[0]
            
            if not ip_address:
                await self.close()
                return

            if not self.user.is_authenticated:
                await self.close()
                return
            
            if self.user.is_patient:
                account = await sync_to_async(
                    lambda: Account.objects.get(id=self.user.id)
                )()
                patient = await sync_to_async(
                    lambda: Patient.objects.get(account=account)
                )()
                if not patient:
                    await self.close()
                self.group_name = f'patient_{patient.id}'
                
                queue = await sync_to_async(
                    lambda: Queue.objects.filter(patient=patient).first()
                )()
                if queue:
                    room = await sync_to_async(
                        lambda: queue.room
                    )()
                    await self.channel_layer.group_add(
                        f'room_patient_{room.id}',
                        self.channel_name
                    )
            elif self.user.is_doctor:
                room = await sync_to_async(
                    lambda: Room.objects.filter(ip_address=ip_address).first()
                )()
                self.group_name = f'room_doctor_{room.id}'
                
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()
            
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "update_filters":
            self.filters = data.get("filters", {})
        
    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        await self.close()
        
    async def queue_update(self, event):
        message = event['message']
        data = message.get("data", None)
        
        if message.get("action") == "deleted":
            await self.send(text_data=json.dumps(message))
        else:
            update = await self.check_filters(data)
            if update:
                await self.send(text_data=json.dumps(message))
            else:
                await self.send(text_data=json.dumps({"action": "deleted", "id": data.get("id")}))
        
        
    @sync_to_async
    def check_filters(self, data):
        if not self.filters or not data:
            return True
        time.sleep(0.2)
        queue = Queue.objects.filter(id=data.get("id")).all()
        filter = QueueFilter(data=self.filters, queryset=queue)
        
        return filter.is_valid() and filter.qs.exists()
        