from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import *
from user_profile.serializers import ListDoctorsSerializer
from .paginations import SearchDoctorsPagination


# Create your views here.

class SearchAllDoctorsView(generics.ListAPIView):
    """Search for doctors with username"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListDoctorsSerializer
    pagination_class = SearchDoctorsPagination

    def get_queryset(self):
        q = self.kwargs.get('q').split()
        if len(q) == 1:  # query = first name or last name or username
            return Doctor.objects.filter(Q(user__username__startswith=q[0]) | Q(user__first_name__startswith=q[0]) | Q(
                user__last_name__startswith=q[0])).order_by('-user__date_joined')
        elif len(q) > 1:  # query = first name + last name
            return Doctor.objects.filter(user__first_name=q[0], user__last_name__startswith=q[1]).order_by(
                '-user__date_joined')


class LimitedSearchDoctorsView(generics.ListAPIView):
    """Search for only 5 doctors"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListDoctorsSerializer
    pagination_class = SearchDoctorsPagination

    def get_queryset(self):
        q = self.kwargs.get('q').split()
        if len(q) == 1:  # query = first name or last name or username
            return Doctor.objects.filter(Q(user__username__startswith=q[0]) | Q(user__first_name__startswith=q[0]) | Q(
                user__last_name__startswith=q[0])).order_by('-user__date_joined')[:5]
        elif len(q) > 1:  # query = first name + last name
            return Doctor.objects.filter(user__first_name=q[0], user__last_name__startswith=q[1]).order_by(
                '-user__date_joined')[:5]
