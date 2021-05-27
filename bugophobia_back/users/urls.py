from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import RateList , RateDetail

urlpatterns = [
    path('register/patient/', views.RegisterPatientView.as_view()),
    path('register/doctor/', views.RegisterDoctorView.as_view()),
    path('token/email/', views.CustomTokenView.as_view(), name='token_obtain_pair_email'),
    path('token/username/', views.UsernameTokenView.as_view(), name='token_obtain_pair_username'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detail/patient/', views.PatientDetailView.as_view()),
    path('detail/doctor/', views.DoctorDetailView.as_view()),
    path('rate-list/' , RateList.as_view(), name= 'rate-list'),
    path('rate-detail/<int:doctor_id>/', RateDetail.as_view(), name = 'rate-detail'),
    path('top-doctor-list/' , views.TopDoctorView.as_view(), name= 'top-doctor-list'),
    path('office-list/' , views.OfficeList.as_view(), name= 'office-list'),
    path('office-list/<int:doctor>/' , views.officeListByDoctorID.as_view(), name= 'office-list'),
    # path('office-detail/<int:pk>/' , views.OfficeDetail.as_view(), name= 'office-detail'),
]
