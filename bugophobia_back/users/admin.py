from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Rate)
admin.site.register(OfficePhone)
admin.site.register(Office)