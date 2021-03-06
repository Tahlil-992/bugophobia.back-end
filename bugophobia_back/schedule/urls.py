from django.urls import path
from . import views

urlpatterns = [
    path('create_reservation/', views.CreateReservationView.as_view()),
    path('create_multiple_reservations/', views.CreateMultipleReservationsView.as_view()),
    path('get_reservation/', views.GetReservationView.as_view()),
    path('list_reservations/<office_id>/', views.ListReservationsView.as_view()),
    path('doctor_reservations/<from_date>/<to_date>/', views.ListDoctorReservationsView.as_view()),
    path('patient_reservations/<from_date>/<to_date>/', views.ListPatientReservationView.as_view()),
    path('office_reservations/<office_id>/<from_date>/<to_date>/', views.ListOfficeReservationsView.as_view()),
    path('delete_reservation/<id>/', views.DeleteReservationView.as_view()),
    path('get-notification/<int:patient>/', views.GetNotificationView.as_view()),
    path('delete-notification/<int:pk>/', views.DeleteNotificationView.as_view()),
    path('unreserve/<id>/', views.UnreserveView.as_view()),
]
