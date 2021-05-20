from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from datetime import timedelta, datetime

from .serializers import *
from .models import Reservation
from users.models import Doctor
from user_profile.permissions import IsDoctor


# Create your views here.
class CreateReservationView(generics.CreateAPIView):
    """Create reservation time for doctor, start time should be like 'year month day hour minute'"""
    permission_classes = [IsAuthenticated, IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = CreateReservationSerializer

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user_id=request.user.id)
        start_time_list = request.data.get('start_time').split()
        start_time = datetime(year=int(start_time_list[0]), month=int(start_time_list[1]), day=int(start_time_list[2]),
                              hour=int(start_time_list[3]), minute=int(start_time_list[4]))
        if doctor.visit_duration_time:
            end_time = start_time + timedelta(minutes=doctor.visit_duration_time)
        else:
            return Response(data={'error': "doctor didn't add visit duration time"},
                            status=status.HTTP_400_BAD_REQUEST)
        q = Reservation.objects.filter(start_time__lte=start_time, end_time__gt=start_time, doctor=doctor)
        if len(q) == 0:
            Reservation.objects.create(doctor=doctor, start_time=start_time, end_time=end_time)
        else:
            return Response(data={'error': 'time conflict'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'detail': 'created'}, status=status.HTTP_201_CREATED)


class GetReservationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ~IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = GetReservationSerializer

    def update(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, id=request.data.get('id'))
        if not reservation.patient:
            patient = get_object_or_404(Patient, user_id=request.user.id)
            reservation.patient = patient
            reservation.save()
            return Response(data={'detail': 'ok'}, status=status.HTTP_200_OK)
        return Response(data={'detail': 'time already taken'}, status=status.HTTP_400_BAD_REQUEST)


class ListReservationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListReservationsSerializer

    def get_queryset(self):
        return Reservation.objects.filter(doctor__user_id=self.kwargs.get('id'))


class ListTakenReservationsView(generics.ListAPIView):
    serializer_class = ListTakenReservationsSerializer

    def get_queryset(self):
        return Reservation.objects.filter(doctor__user_id=self.kwargs.get('id'), patient__isnull=False)
