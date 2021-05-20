from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from users.serializers import DoctorDetailSerializer


class CommentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(max_length=255)

    class Meta:
        model = Comment
        fields = ['doctor', 'comment_text']


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'city', 'is_doctor')


class PublicBaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'phone_number', 'gender', 'age', 'city')


# patient profile

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


class ListCommentSerializer(serializers.ModelSerializer):
    patient = PublicPatientProfileSerializer(read_only=True)
    doctor_username = serializers.CharField(write_only=True)
    comment_text = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'created', 'patient', 'doctor_username')


class DeleteUpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_text']


class SaveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveProfile
        fields = ['id', 'doctor', 'created']


class ListSavedProfileSerializer(serializers.ModelSerializer):
    doctor = DoctorDetailSerializer()

    class Meta:
        model = SaveProfile
        fields = ['id', 'doctor']


class ListDoctorsSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'filed_of_specialization', 'gmc_number', 'work_experience']


# doctor profile

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Doctor
        fields = ('user', 'gmc_number', 'filed_of_specialization', 'work_experience')


class PublicDoctorProfileSerializer(serializers.ModelSerializer):
    user = PublicBaseUserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    filed_of_specialization = serializers.CharField(read_only=True)
    work_experience = serializers.IntegerField(read_only=True)
    gmc_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Doctor
        fields = ('user', 'username', 'gmc_number', 'filed_of_specialization', 'work_experience')


class UpdateDoctorProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [ 'city' , 'phone_number' , 'username' , 'email' , 'pro_picture']


class UpdatePatientProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'username', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'city' , 'pro_picture']
