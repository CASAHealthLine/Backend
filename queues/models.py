from django.db import models

class Queue(models.Model):
    STATUS_CHOICES = [
        (0, 'In Progress'),
        (1, 'Waiting'),
        (2, 'Completed'),
        (3, 'Cancelled'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='queues')
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='queues')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Patient {self.patient.full_name} - Room {self.room.displayname}'
