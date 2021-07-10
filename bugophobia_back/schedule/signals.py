from django.core.checks import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification,Reservation
from django.utils import timezone
import pdb

@receiver(post_save,sender=Reservation)
def on_create_reservation(sender,instance,created,*args,**kwargs):
     if created:
          present_time=timezone.now()
          reservation_time=instance.start_time
          Notification.objects.create(
               patient=instance.patient,
               reservation=instance,
               doctor=instance.doctor,
               message=f"there is {reservation_time-present_time} time left to appointment with doctor {instance.doctor.user.username}"
          )
          