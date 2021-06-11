from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import *
from user_profile.serializers import ListDoctorsSerializer
from .paginations import SearchDoctorsPagination


# Create your views here.

class SearchAllDoctorsView(generics.ListAPIView):
    """Search for doctors url should be like /all/?q=username&gender=M&specialization=G&city=Tehran"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListDoctorsSerializer
    pagination_class = SearchDoctorsPagination

    def get_queryset(self):
        try:
            q = self.request.query_params.get('q').split()
        except AttributeError:
            return Doctor.objects.all()
        if len(q) == 1:  # query = first name or last name or username
            return Doctor.objects.filter(
                Q(user__username__startswith=q[0]) | Q(user__first_name__startswith=q[0]) | Q(
                    user__last_name__startswith=q[0])).order_by('-rate_avg')
        elif len(q) > 1:  # query = first name + last name
            return Doctor.objects.filter(user__first_name=q[0], user__last_name__startswith=q[1]).order_by(
                '-rate_avg')

    def filter_queryset(self, queryset):
        filters = self.request.query_params
        gender = filters.get('gender')
        city = filters.get('city')
        specialization = filters.get('specialization')
        if gender:
            queryset = queryset.filter(user__gender=gender)
        if city:
            queryset = queryset.filter(user__city=city)
        if specialization:
            queryset = queryset.filter(filed_of_specialization=specialization)
        return queryset


class LimitedSearchDoctorsView(generics.ListAPIView):
    """Search for only 5 doctors"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListDoctorsSerializer

    def get_queryset(self):
        try:
            q = self.request.query_params.get('q').split()
        except AttributeError:
            return Doctor.objects.all()[:5]
        if len(q) == 1:  # query = first name or last name or username
            return Doctor.objects.filter(
                Q(user__username__startswith=q[0]) | Q(user__first_name__startswith=q[0]) | Q(
                    user__last_name__startswith=q[0])).order_by('-rate_avg')[:5]
        elif len(q) > 1:  # query = first name + last name
            return Doctor.objects.filter(user__first_name=q[0], user__last_name__startswith=q[1]).order_by(
                '-rate_avg')[:5]

    def filter_queryset(self, queryset):
        filters = self.request.query_params
        gender = filters.get('gender')
        city = filters.get('city')
        specialization = filters.get('specialization')
        if gender:
            queryset = queryset.filter(user__gender=gender)
        if city:
            queryset = queryset.filter(user__city=city)
        if specialization:
            queryset = queryset.filter(filed_of_specialization=specialization)
        return queryset
