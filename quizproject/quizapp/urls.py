from django.urls import path
from . import views

urlpatterns = [
    path('', views.loadQuestions, name='home'),
    path('restart/', views.restart, name='restart'),
    path('checkAnswer/', views.checkAnswer, name='checkAnswer'),
]