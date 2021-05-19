from django.urls import path
from . import views

urlpatterns = [
    path('create_reservation/', views.CreateReservationView.as_view()),
    path('get_reservation/', views.GetReservationView.as_view()),
    path('list_reservations/<id>/', views.ListReservationsView.as_view()),
]
