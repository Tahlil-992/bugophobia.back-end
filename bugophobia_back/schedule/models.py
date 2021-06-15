from django.db import models
from users.models import Doctor, Patient, Office
import pytz
from datetime import datetime


# Create your models here.

class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['start_time']
        unique_together = ['doctor', 'start_time']


class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now(tz=pytz.utc))
