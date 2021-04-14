from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.CreateCommentView.as_view()),
]
