from django.contrib import admin
from .models import BaseUser, Patient, Doctor

# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Patient)
admin.site.register(Doctor)
