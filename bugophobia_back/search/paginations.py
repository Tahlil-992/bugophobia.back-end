from rest_framework.pagination import PageNumberPagination


class SearchDoctorsPagination(PageNumberPagination):
    page_size = 10
