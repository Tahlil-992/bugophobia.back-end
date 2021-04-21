from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

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


class PublicPatientProfileView(generics.RetrieveAPIView):
    """Returns patient profile to doctors"""
    permission_classes = [IsAuthenticated, IsDoctor]
    authentication_classes = [JWTTokenUserAuthentication]
    queryset = Patient.objects.all()
    serializer_class = PublicPatientProfileSerializer

    def get_object(self):
        patient_user = get_object_or_404(BaseUser, username=self.request.data.get('username'))
        patient = get_object_or_404(Patient, user=patient_user)
        return patient


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
