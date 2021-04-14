from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *


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
