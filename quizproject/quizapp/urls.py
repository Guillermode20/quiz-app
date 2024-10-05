from django.urls import path
from . import views

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('quiz/', views.loadQuestions, name='loadQuestions'),
    path('restart/', views.restart, name='restart'),
    path('checkAnswer/', views.checkAnswer, name='checkAnswer'),
]