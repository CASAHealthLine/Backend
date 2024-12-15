from django.db import models

class RoomType(models.Model):
    type_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type_name

class Room(models.Model):
    displayname = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.displayname
