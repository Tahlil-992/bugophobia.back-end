from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from datetime import timedelta, datetime
from pytz import UTC

from .serializers import *
from .models import Reservation
from users.models import Doctor
from user_profile.permissions import IsDoctor, IsOwner


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
        office = get_object_or_404(Office, id=request.data.get('office'))
        if doctor.visit_duration_time:
            end_time = start_time + timedelta(minutes=doctor.visit_duration_time)
        else:
            return Response(data={'error': "doctor didn't add visit duration time"},
                            status=status.HTTP_400_BAD_REQUEST)
        q = Reservation.objects.filter(start_time__lte=start_time, end_time__gt=start_time, doctor=doctor)
        if len(q) == 0:
            obj = Reservation.objects.create(doctor=doctor, start_time=start_time, end_time=end_time, office=office)
        else:
            return Response(data={'error': 'time conflict'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GetReservationView(generics.UpdateAPIView):
    """Taking reservations view"""
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
    """List all available reservations to patients"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListReservationsSerializer

    def get_queryset(self):
        return Reservation.objects.filter(office__id=self.kwargs.get('office_id'), start_time__gt=datetime.now(),
                                          patient__isnull=True)


class ListDoctorReservationsView(generics.ListAPIView):
    """List doctor's reservations"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = ListTakenReservationsSerializer

    def get_queryset(self):
        from_date_str = self.kwargs.get('from_date')  # YYYYMMDD
        from_date = datetime(year=int(from_date_str[:4]), month=int(from_date_str[4:6]), day=int(from_date_str[6:]),
                             hour=0, minute=0)
        to_date_str = self.kwargs.get('to_date')  # YYYYMMDD
        to_date = datetime(year=int(to_date_str[:4]), month=int(to_date_str[4:6]), day=int(to_date_str[6:]), hour=0,
                           minute=0)
        return Reservation.objects.filter(doctor__user_id=self.request.user.id,
                                          start_time__gt=from_date,
                                          start_time__lt=to_date)


class ListOfficeReservationsView(generics.ListAPIView):
    """List doctor's reservations"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = ListTakenReservationsSerializer

    def get_queryset(self):
        from_date_str = self.kwargs.get('from_date')  # YYYYMMDD
        from_date = datetime(year=int(from_date_str[:4]), month=int(from_date_str[4:6]), day=int(from_date_str[6:]),
                             hour=0, minute=0)
        to_date_str = self.kwargs.get('to_date')  # YYYYMMDD
        to_date = datetime(year=int(to_date_str[:4]), month=int(to_date_str[4:6]), day=int(to_date_str[6:]), hour=0,
                           minute=0)
        return Reservation.objects.filter(office__id=self.kwargs.get('office_id'), start_time__gt=from_date,
                                          start_time__lt=to_date)


class ListPatientReservationView(generics.ListAPIView):
    """List patient reservations"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = ListPatientReservationSerializer

    def get_queryset(self):
        from_date_str = self.kwargs.get('from_date')  # YYYYMMDD
        from_date = datetime(year=int(from_date_str[:4]), month=int(from_date_str[4:6]), day=int(from_date_str[6:]),
                             hour=0, minute=0)
        to_date_str = self.kwargs.get('to_date')  # YYYYMMDD
        to_date = datetime(year=int(to_date_str[:4]), month=int(to_date_str[4:6]), day=int(to_date_str[6:]), hour=0,
                           minute=0)
        return Reservation.objects.filter(patient__user_id=self.request.user.id, start_time__gt=from_date,
                                          start_time__lt=to_date)


class DeleteReservationView(generics.DestroyAPIView):
    """Delete not taken reservations"""
    permission_classes = [IsAuthenticated, IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = GetReservationSerializer

    def get_object(self):
        obj = get_object_or_404(Reservation, doctor__user_id=self.request.user.id, id=self.kwargs.get('id'))
        if obj.patient:
            return None
        return obj

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            self.perform_destroy(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'detail': "You can't delete a time that has a patient"},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateMultipleReservationsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = CreateReservationSerializer

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user_id=request.user.id)
        start_time_list = request.data.get('start_time').split()
        start_time = datetime(year=int(start_time_list[0]), month=int(start_time_list[1]), day=int(start_time_list[2]),
                              hour=int(start_time_list[3]), minute=int(start_time_list[4]))
        end_time_list = request.data.get('end_time').split()
        end_time = datetime(year=int(end_time_list[0]), month=int(end_time_list[1]), day=int(end_time_list[2]),
                            hour=int(end_time_list[3]), minute=int(end_time_list[4]))
        office = get_object_or_404(Office, id=request.data.get('office'))
        if not doctor.visit_duration_time:
            return Response(data={'error': "doctor didn't add visit duration time"}, status=status.HTTP_400_BAD_REQUEST)
        objs = []
        while start_time < end_time:
            q = Reservation.objects.filter(start_time__lte=start_time, end_time__gt=start_time, doctor=doctor)
            end_time_temp = start_time + timedelta(minutes=doctor.visit_duration_time)
            if len(q) == 0:
                objs.append(Reservation.objects.create(doctor=doctor, start_time=start_time, end_time=end_time_temp,
                                                       office=office))
            start_time = end_time_temp

        serializer = self.serializer_class(objs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UnreserveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = GetReservationSerializer

    def get_object(self):
        r = get_object_or_404(Reservation, id=self.kwargs.get('id'))
        self.check_object_permissions(self.request, r)
        if r.start_time > UTC.localize(datetime.now()):
            r.patient = None
            r.save()
            return r
        return None

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        s = self.serializer_class(obj)
        if obj:
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'reservation time has passed'}, status=status.HTTP_400_BAD_REQUEST)
