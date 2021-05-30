from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from users.models import *
from user_profile.serializers import BaseUserSerializer


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('start_time', 'id')


class GetReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id',)


class ListReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'start_time', 'end_time')


class BaseUserReservationSerializer(BaseUserSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'first_name', 'last_name')


class PatientReservationSerializer(serializers.ModelSerializer):
    user = BaseUserReservationSerializer()

    class Meta:
        model = Patient
        fields = ('user',)


class DoctorReservationSerializer(serializers.ModelSerializer):
    user = BaseUserReservationSerializer()

    class Meta:
        model = Doctor
        fields = ('user', 'filed_of_specialization')


class ListTakenReservationsSerializer(serializers.ModelSerializer):
    patient = PatientReservationSerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'patient', 'start_time', 'end_time')


class ListPatientReservationSerializer(serializers.ModelSerializer):
    doctor = DoctorReservationSerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'start_time', 'end_time', 'doctor')
