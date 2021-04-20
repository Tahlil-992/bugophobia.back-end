from rest_framework import serializers
from .models import Patient, BaseUser, Doctor ,Rate


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
        fields = ['user', 'gmc_number', 'filed_of_specialization' , 'work_experience']


class RegisterDoctorSerializer(serializers.ModelSerializer):
    user = RegisterBaseUserSerializer()

    class Meta:
        model = Doctor
        fields = ('user', 'gmc_number', 'filed_of_specialization' , 'work_experience')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data['password']
        user = BaseUser(**user_data)
        if password is not None:
            user.set_password(password)
        user.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor



#rate

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id' , 'amount']



class RateAverageSerializer(serializers.Serializer):
    rate__avg = serializers.FloatField()
    
    def create(self , validated_data):
        return super().create(validated_data)

    def update(self , instance , validated_data):
        instance.rate__avg = validated_data.get('rate__avg' , instance.rate__avg)
        instance.save()
        return instance
