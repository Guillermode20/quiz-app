from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.loadQuestions, name='loadQuestions'),
    path('restart/', views.restart, name='restart'),
    path('checkAnswer/', views.checkAnswer, name='checkAnswer'),
    path('', views.startpage, name='startpage'),
    path('trivia/', views.get_trivia_questions, name='trivia'),
    ]