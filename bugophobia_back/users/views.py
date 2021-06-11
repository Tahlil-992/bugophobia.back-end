from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import string
import random

from .models import Patient, Doctor
from .serializers import *
from bugophobia_back.settings import EMAIL_HOST_USER
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


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordUserSerializer
    queryset = ResetPasswordToken.objects.all()

    def post(self, request):
        serializer = self.serializer_class(request.data)
        ResetPasswordToken.objects.filter(user__email=serializer.data.get('email')).delete()
        is_different = True
        while is_different:
            token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            token_query = ResetPasswordToken.objects.filter(token=token)
            if token_query:
                is_different = True
            else:
                is_different = False
        user = get_object_or_404(BaseUser, email=serializer.data.get('email'))
        message = f'Use the link below to reset your password:\nlocalhost:3000/forget-password/{token}'
        context = {'token': token}
        html_message = render_to_string('email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(
            'Reset password code',
            plain_message,
            EMAIL_HOST_USER,
            [request.data.get('email')],
            html_message=html_message,
            fail_silently=False,
        )
        ResetPasswordToken.objects.create(token=token, user=user, expiry_time=datetime.now() + timedelta(minutes=2))
        return Response(status=status.HTTP_200_OK)


class ConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = ConfirmResetPasswordUserSerializer
    queryset = BaseUser.objects.all()

    def post(self, request, token):
        reset_password_token = get_object_or_404(ResetPasswordToken, token=token)
        if reset_password_token.expiry_time > datetime.now(reset_password_token.expiry_time.tzinfo):
            user = reset_password_token.user
            if request.data.get('password') is not None:
                user.set_password(request.data.get('password'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            reset_password_token.delete()
            return Response(data={'detail': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)
