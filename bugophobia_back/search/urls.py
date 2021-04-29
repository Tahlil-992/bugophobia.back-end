from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.SearchView.as_view()),
]
