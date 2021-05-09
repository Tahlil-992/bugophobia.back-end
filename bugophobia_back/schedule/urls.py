from django.urls import path
from . import views

urlpatterns = [
    path('create_reservation/', views.CreateReservationView.as_view()),
]
