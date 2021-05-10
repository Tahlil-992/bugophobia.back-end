from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Patient, Doctor
from .serializers import *
from django.db.models import Avg


class UsernameTokenView(APIView):
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        if request.data.get('username', None):
            user = get_object_or_404(BaseUser, username=request.data.get('username'))
        else:
            return Response(data={'username': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if password:
            if user.check_password(request.data.get('password')):
                return Response(data=self.get_tokens_for_user(user), status=status.HTTP_200_OK)
            else:
                return Response(data={"detail": 'Not found.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"password": 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


# patient

class PatientDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = PatientDetailSerializer

    def get(self, request):
        user = get_object_or_404(BaseUser, id=request.user.id)
        patient = get_object_or_404(Patient, user=user)
        serializer = PatientDetailSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = RegisterPatientSerializer


# doctor

class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = DoctorDetailSerializer

    def get(self, request):
        user = get_object_or_404(BaseUser, id=request.user.id)
        doctor = get_object_or_404(Doctor, user=user)
        serializer = DoctorDetailSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = RegisterDoctorSerializer


# rate

class RateList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Rate.objects.all()
    serializer_class = ScoreSerializer

    def create(self, request):
        user_id = request.user.id
        doctor_id = request.data.get('doctor_id')
        rate = Rate.objects.filter(user_id=user_id, doctor_id=doctor_id)
        serializer = ScoreSerializer(
            data={'user_id': user_id, 'doctor_id': doctor_id, 'amount': request.data.get('amount')})
        if rate:
            return Response(status=status.HTTP_409_CONFLICT)
        elif serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RateDetail(APIView):
    def get(self, request, doctor_id, format=None):
        avg = Rate.objects.filter(doctor_id=doctor_id).aggregate(Avg('amount'))
        number = Rate.objects.filter(doctor_id=doctor_id).count()
        data = {'avg': avg.get("amount__avg"), 'number': number}
        serializer = ScoreAverageSerializer(data)
        return Response(serializer.data)
