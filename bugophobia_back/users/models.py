from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Patient(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Doctor(AbstractUser):
    email = models.EmailField(max_length=255 , unique=True)
    username = models.CharField(max_length=255 , unique= True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    