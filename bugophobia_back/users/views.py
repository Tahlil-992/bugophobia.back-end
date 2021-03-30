from django.shortcuts import render
from rest_framework import generics
from .models import Patient
from .serializers import RegisterPatientSerializer


# Create your views here.

class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = RegisterPatientSerializer
