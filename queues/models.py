from django.db import models
from django.utils.timezone import now

class Queue(models.Model):
    STATUS_CHOICES = [
        (0, 'In Progress'),
        (1, 'Waiting'),
        (2, 'Completed'),
        (3, 'Cancelled'),
    ]

    order = models.PositiveIntegerField(default=1)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='queues')
    health_record = models.ForeignKey('patients.HealthRecord', on_delete=models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='queues')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_order = Queue.objects.filter(
                room=self.room,
                date=now().date(),
            ).aggregate(models.Max('order'))['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Patient {self.patient.full_name} - Room {self.room.displayname}'
