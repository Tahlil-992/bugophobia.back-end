from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .models import *
from bugophobia_back.settings import EMAIL_HOST_USER


class RegisterBaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'city',
                  'is_doctor', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


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
        fields = ['user', 'gmc_number', 'filed_of_specialization', 'work_experience', 'rate_avg']


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
        doctor = Doctor.objects.create(user=user, is_confirmed=False, **validated_data)
        superusers_emails = BaseUser.objects.filter(is_superuser=True).values_list('email')
        superusers_emails = [i[0] for i in superusers_emails]
        user_data.update(validated_data)
        html_message = render_to_string('doctor_request.html', user_data)
        plain_message = strip_tags(html_message)
        send_mail('a doctor wants to sign up',
                  plain_message,
                  EMAIL_HOST_USER,
                  superusers_emails,
                  html_message=html_message,
                  fail_silently=False,
                  )
        return doctor


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_doctor'] = self.user.is_doctor
        if self.user.is_doctor:
            if Doctor.objects.get(user=self.user).is_confirmed:
                return data
            data['refresh'] = None
            data['access'] = None
            return data
        return data


# rate

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class ScoreAverageSerializer(serializers.Serializer):
    avg = serializers.FloatField()
    number = serializers.IntegerField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ForgotPasswordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email']


class ConfirmResetPasswordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}


class TopDoctorSerializer(serializers.ModelSerializer):
    avg = serializers.FloatField(default=0.0)
    number = serializers.IntegerField(default=0)

    class Meta:
        model = Doctor
        fields = ['user', 'filed_of_specialization', 'gmc_number', 'work_experience', 'avg', 'number']


class OfficePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficePhone
        fields = ['id', 'phone']


class OfficeSerialzier(serializers.ModelSerializer):
    phone = OfficePhoneSerializer(many=True)

    def create(self, validated_data):
        phones = validated_data.pop('phone')
        office = Office.objects.create(**validated_data)
        for data in phones:
            p = OfficePhone(phone=data['phone'], office=office)
            p.save()
        return office

    def update(self, instance, validated_data):
        phone_numbers = validated_data.pop('phone')
        OfficePhone.objects.filter(office=instance.id).delete()
        for data in phone_numbers:
            OfficePhone.objects.create(office=instance, phone=data.get('phone'))
        return super().update(instance, validated_data)

    class Meta():
        model = Office
        fields = ['id', 'doctor', 'title', 'address', 'location', 'phone']
        lookup_field = 'doctor'
