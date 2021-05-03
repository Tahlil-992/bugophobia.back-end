from django.urls import path
from . import views

urlpatterns = [
    path('all/<q>/', views.SearchAllDoctorsView.as_view()),
    path('limited/<q>/', views.LimitedSearchDoctorsView.as_view()),
]
