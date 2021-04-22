from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.CreateCommentView.as_view()),
    path('comments/', views.ListCommentView.as_view()),
    path('comment/update_delete/<id>/', views.DeleteUpdateCommentView.as_view()),
    path('patient/', views.PatientProfileView.as_view()),
    path('patient/public/', views.PublicPatientProfileView.as_view()),
    path('doctor/', views.DoctorProfileView.as_view()),
    path('doctor/public/', views.PublicDoctorProfileView.as_view()),
]
