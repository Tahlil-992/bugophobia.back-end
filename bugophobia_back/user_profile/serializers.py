from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(max_length=255)

    class Meta:
        model = Comment
        fields = ['doctor', 'comment_text']


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'city', 'is_doctor')


class PublicBaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'first_name', 'last_name', 'gender', 'age', 'city')


class PatientProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Patient
        fields = ('user', 'insurance_type')


class PublicPatientProfileSerializer(serializers.ModelSerializer):
    user = PublicBaseUserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    insurance_type = serializers.CharField(read_only=True)

    class Meta:
        model = Patient
        fields = ('user', 'username', 'insurance_type')
