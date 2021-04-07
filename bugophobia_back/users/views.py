from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import Patient , Doctor
from .serializers import *




# class RegisterPatientView(generics.CreateAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = RegisterPatientSerializer
#
#

#patient

class PatientDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = PatientDetailSerializer

    def get(self, request):
        user = get_object_or_404(BaseUser, id=request.user.id)
        patient = get_object_or_404(Patient, user=user)
        serializer = PatientDetailSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = RegisterPatientSerializer


#doctor

class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = DoctorDetailSerializer

    def get(self, request):
        user = get_object_or_404(BaseUser, id=request.user.id)
        doctor = get_object_or_404(Doctor, user=user)
        serializer = DoctorDetailSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = RegisterDoctorSerializer
