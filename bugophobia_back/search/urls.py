from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.SearchAllDoctorsView.as_view()),
    path('limited/', views.LimitedSearchDoctorsView.as_view()),
]
