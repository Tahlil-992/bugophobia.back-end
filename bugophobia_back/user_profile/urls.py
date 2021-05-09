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
    path('save/', views.SaveProfileView.as_view()),
    path('remove_save/<id>/', views.RemoveSavedProfileView.as_view()),
    path('is_saved/', views.IsProfileSavedView.as_view()),
    path('list_doctors/', views.ListDoctorsView.as_view()),
    path('doctor/update/<id>/', views.UpdateDoctorProfView.as_view()),
    path('patient/update/<id>/', views.UpdatePatientProfView.as_view()),
]
