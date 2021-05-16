from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from datetime import timedelta, datetime

from .serializers import *
from .models import Reservation
from users.models import Doctor


# Create your views here.
class CreateReservationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = CreateReservationSerializer

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user_id=request.user.id)
        start_time = datetime.fromtimestamp(int(request.data.get('start_time')) / 1000)
        end_time = start_time + timedelta(minutes=doctor.visit_duration_time)
        Reservation.objects.create(doctor=doctor, start_time=start_time, end_time=end_time)
        return Response(data={'detail': 'created'}, status=status.HTTP_201_CREATED)


class GetReservationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = GetReservationSerializer

    def update(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user_id=request.user.id)
        reservation = get_object_or_404(Reservation, id=request.data.get('id'))
        reservation.patient = patient
        reservation.save()
        return Response(data={'detail': 'ok'}, status=status.HTTP_200_OK)
