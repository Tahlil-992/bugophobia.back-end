from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.CreateCommentView.as_view()),
    path('patient/', views.PatientProfileView.as_view()),
    path('patient/public/', views.PublicPatientProfileView.as_view()),
]
