from django.contrib import admin
from .models import BaseUser, Patient, Doctor ,Rate
# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Rate)