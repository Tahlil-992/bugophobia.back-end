from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterPatientView.as_view()),
]