from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class BaseUser(AbstractUser):
    GENDERS = [('M', 'Male'),
               ('F', 'Female')]

    pro_picture = models.ImageField(null=True, blank=True, upload_to="images")
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDERS, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Patient(models.Model):
    INSURANCE_TYPES = [('O', 'omr'),
                       ('H', 'havades'),
                       ('T', 'takmili')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    insurance_type = models.CharField(max_length=255, choices=INSURANCE_TYPES, default='O', null=True, blank=True)

    def __str__(self):
        return self.user.email


class Doctor(models.Model):
    FILED_OF_SPECIALIZATION = [
        ('C', 'Cardiologist'),
        ('D', 'Dermatologist'),
        ('G', 'General practitioner'),
        ('GY', 'Gynecologist'),
        ('I', 'Internist'),
        ('N', 'Neurologist'),
        ('O', 'Obstetrician'),
        ('OP', 'Ophthalmologist'),
        ('OT', 'Otolaryngologist'),
        ('P', 'Pediatrician '),
        ('PS', 'Psychiatrist '),
        ('U', 'Urologist'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    filed_of_specialization = models.CharField(max_length=255, choices=FILED_OF_SPECIALIZATION, default='G', null=False,
                                               blank=False)
    gmc_number = models.IntegerField(null=False)
    work_experience = models.IntegerField(default=0, null=False)
    visit_duration_time = models.IntegerField(null=True)
    rate_avg = models.FloatField(default=0.0)
    is_confirmed = models.BooleanField()

    def __str__(self):
        return self.user.email


class Rate(models.Model):
    SCORES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    amount = models.IntegerField(default=1, choices=SCORES)
    user_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)


class ResetPasswordToken(models.Model):
    token = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    expiry_time = models.DateTimeField()


class Office(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address = models.TextField()
    location = models.FloatField()

    def __str__(self):
        return f"{self.title}({self.id})"


class OfficePhone(models.Model):
    office = models.ForeignKey(Office, related_name='phone', on_delete=models.CASCADE)
    phone = models.TextField()
