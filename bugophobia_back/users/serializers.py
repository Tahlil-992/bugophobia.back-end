from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *


class RegisterBaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'username', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'city', 'is_doctor',
                  'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class BaseUserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['username']


# patient

class PatientDetailSerializer(serializers.ModelSerializer):
    user = RegisterBaseUserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'insurance_type']


class RegisterPatientSerializer(serializers.ModelSerializer):
    user = RegisterBaseUserSerializer()

    class Meta:
        model = Patient
        fields = ('user', 'insurance_type')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data['password']
        user = BaseUser(**user_data)
        if password is not None:
            user.set_password(password)
        user.save()
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


# doctor

class DoctorDetailSerializer(serializers.ModelSerializer):
    user = RegisterBaseUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'gmc_number', 'filed_of_specialization', 'work_experience']


class RegisterDoctorSerializer(serializers.ModelSerializer):
    user = RegisterBaseUserSerializer()

    class Meta:
        model = Doctor
        fields = ('user', 'gmc_number', 'filed_of_specialization', 'work_experience')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data['password']
        user = BaseUser(**user_data)
        if password is not None:
            user.set_password(password)
        user.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor


class DoctorUsernameSerializer(serializers.ModelSerializer):
    user = BaseUserUsernameSerializer()

    class Meta:
        model = Doctor
        fields = ['user']


class PatientUsernameSerializer(serializers.ModelSerializer):
    user = BaseUserUsernameSerializer()

    class Meta:
        model = Patient
        fields = ['user']


class CommentSerializer(serializers.ModelSerializer):
    # doctor = DoctorUsernameSerializer()
    # writer = PatientUsernameSerializer()
    # doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    # patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    doctor = serializers.CharField(max_length=255)
    patient = serializers.CharField(max_length=255)

    class Meta:
        model = Comment
        fields = ['doctor', 'patient', 'comment_text']

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor')
        patient_data = validated_data.pop('patient')
        doctor_base_user = get_object_or_404(BaseUser, username=doctor_data)
        patient_base_user = get_object_or_404(BaseUser, username=patient_data)
        doctor_user = get_object_or_404(Doctor, user=doctor_base_user)
        patient_user = get_object_or_404(Patient, user=patient_base_user)
        comment = Comment.objects.create(doctor=doctor_user, patient=patient_user, **validated_data)
        return comment
