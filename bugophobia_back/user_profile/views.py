from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.generics import UpdateAPIView

from .models import *
from .serializers import *
from .permissions import *
from .paginations import *


# Create your views here.


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        patient_user = get_object_or_404(BaseUser, id=request.user.id)
        patient = get_object_or_404(Patient, user=patient_user)
        doctor_user = get_object_or_404(BaseUser, username=request.data.get('doctor'))
        doctor = get_object_or_404(Doctor, user=doctor_user)
        cm_text = request.data.get('comment_text')
        Comment.objects.create(doctor=doctor, patient=patient, comment_text=cm_text)
        return Response(data={'detail': 'comment has created'}, status=status.HTTP_201_CREATED)


class PatientProfileView(generics.RetrieveAPIView):
    """Return patient profile to himself"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Patient.objects.all()
    serializer_class = PatientProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        patient_user = get_object_or_404(BaseUser, id=request.user.id)
        patient = get_object_or_404(Patient, user=patient_user)
        serializer = self.serializer_class(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicPatientProfileView(generics.GenericAPIView):
    """Returns patient profile to doctors"""
    permission_classes = [IsAuthenticated, IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Patient.objects.all()
    serializer_class = PublicPatientProfileSerializer

    def get_object(self):
        patient_user = get_object_or_404(BaseUser, username=self.request.data.get('username'))
        patient = get_object_or_404(Patient, user=patient_user)
        return patient

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCommentView(generics.GenericAPIView):
    """List all comments of a specific doctor with getting doctor username"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = ListCommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        doctor_user = get_object_or_404(BaseUser, username=self.request.data.get('doctor_username'))
        doctor = get_object_or_404(Doctor, user=doctor_user)
        return Comment.objects.filter(doctor=doctor)

    def post(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(self.get_queryset())
        serializer = ListCommentSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class DeleteUpdateCommentView(generics.RetrieveUpdateDestroyAPIView):
    """"Delete comment with delete method and update comment with put & patch method and get specific comment with
    get """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = DeleteUpdateCommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'


class DoctorProfileView(generics.RetrieveAPIView):
    """Return Doctor profile to himself"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        doctor_user = get_object_or_404(BaseUser, id=request.user.id)
        doctor = get_object_or_404(Doctor, user=doctor_user)
        serializer = self.serializer_class(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicDoctorProfileView(generics.GenericAPIView):
    """Returns doctor profile to patient"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Doctor.objects.all()
    serializer_class = PublicDoctorProfileSerializer

    def get_object(self):
        doctor_user = get_object_or_404(BaseUser, username=self.request.data.get('username'))
        doctor = get_object_or_404(Doctor, user=doctor_user)
        return doctor

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveProfileView(generics.ListCreateAPIView):
    """Save doctor's profile with get method and Returns User's saved profiles with get method"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = SaveProfile.objects.all()
    serializer_class = SaveProfileSerializer

    def create(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user_id=request.user.id)
        doctor_base_user = get_object_or_404(BaseUser, username=request.data.get('doctor'))
        doctor = get_object_or_404(Doctor, user=doctor_base_user)
        try:
            s = SaveProfile.objects.create(patient=patient, doctor=doctor)
            serializer = self.serializer_class(s)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'error': 'user has already saved the profile'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user_id=request.user.id)
        queryset = SaveProfile.objects.filter(patient=patient)
        serializer = ListSavedProfileSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RemoveSavedProfileView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = SaveProfile.objects.all()
    serializer_class = SaveProfileSerializer
    lookup_field = 'id'


class IsProfileSavedView(APIView):
    """Gets 'doctor_username' and checks if user has saved it or not"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user_id=request.user.id)
        doctor_base_user = get_object_or_404(BaseUser, username=request.data.get("doctor_username"))
        doctor = get_object_or_404(Doctor, user=doctor_base_user)
        q = SaveProfile.objects.filter(patient=patient, doctor=doctor)
        if q.count() > 0:
            return Response(data={'saved': True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'saved': False}, status=status.HTTP_200_OK)


class ListDoctorsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = ListDoctorsSerializer


class ChangeVisitDurationTimeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    queryset = Doctor.objects.all()
    serializer_class = ChangeVisitDurationTimeSerializer

    def get_object(self):
        doctor = get_object_or_404(Doctor, user_id=self.request.user.id)
        return doctor


#edit profile
class UpdateDoctorProfView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, IsOwner]
    queryset = BaseUser.objects.filter(is_doctor=True)
    serializer_class = UpdateDoctorProfSerializer
    lookup_field = 'username'
    

class UpdatePatientProfView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, IsOwner]
    queryset = BaseUser.objects.filter(is_doctor = False)
    serializer_class = UpdatePatientProfSerializer
    lookup_field = 'username'


#change pass

class ChangePasswordView(UpdateAPIView):

        serializer_class = ChangePasswordSerializer
        model = BaseUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)