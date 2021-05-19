from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('start_time',)


class GetReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id',)


class ListReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'start_time', 'end_time')
