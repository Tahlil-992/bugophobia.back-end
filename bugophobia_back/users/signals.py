from django.db.models.signals import post_delete, post_save,post_migrate
from django.dispatch import receiver
from .models import Rate,Doctor


@receiver(post_save,sender=Rate)
def create_rate(sender,instance,created,*args,**kwargs):
    rates=Rate.objects.filter(doctor_id=instance.doctor_id)
    avg=sum([rate.amount for rate in rates])/len(rates)
    Doctor.objects.filter(user_id=instance.doctor_id).update(rate_avg=avg)


@receiver(post_delete,sender=Rate)
def delete_rate(sender,instance,*args, **kwargs):
    rates=Rate.objects.filter(doctor_id=instance.doctor_id)
    avg=sum([rate.amount for rate in rates])/len(rates)
    Doctor.objects.filter(user_id=instance.doctor_id).update(rate_avg=avg)