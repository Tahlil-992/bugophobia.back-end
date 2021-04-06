from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class BaseUser(AbstractUser):
    GENDERS = [('M', 'Male'),
               ('F', 'Female')]
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDERS, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Patient(models.Model):
    INSURANCE_TYPES = [('O', 'omr'),
                       ('H', 'havades'),
                       ('T', 'takmili')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    insurance_type = models.CharField(max_length=255, choices=INSURANCE_TYPES, default='O', null=True, blank=True)

    def __str__(self):
        return self.user.email

# class Doctor(AbstractUser):
#     email = models.EmailField(max_length=255, unique=True)
#     username = models.CharField(max_length=255, unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     def __str__(self):
#         return self.email
