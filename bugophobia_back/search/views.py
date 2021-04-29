from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import *
from user_profile.serializers import ListDoctorsSerializer


# Create your views here.

class SearchView(generics.ListAPIView):
    """Search for doctors with username"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListDoctorsSerializer

    def get_queryset(self):
        return Doctor.objects.filter(user__username__icontains=self.kwargs.get('username'))
