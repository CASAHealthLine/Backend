from django.db import models

class Queue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='queues')
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='queues')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Patient {self.patient.full_name} - Room {self.room.display_name}'
