from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/patient/', views.RegisterPatientView.as_view()),
    path('register/doctor/', views.RegisterDoctorView.as_view()),
    path('token/email/', TokenObtainPairView.as_view(), name='token_obtain_pair_email'),
    path('token/username/', views.UsernameTokenView.as_view(), name='token_obtain_pair_username'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detail/patient/', views.PatientDetailView.as_view()),
    path('detail/doctor/', views.DoctorDetailView.as_view()),
    path('comment/', views.CreateCommentView.as_view()),
]
