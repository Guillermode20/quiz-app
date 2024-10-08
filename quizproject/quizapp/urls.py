from django.urls import path
from . import views

urlpatterns = [
    path('restart/', views.restart, name='restart'),
    path('', views.startpage, name='startpage'),
    path('trivia/', views.get_trivia_questions, name='trivia'),
    path('check_trivia_answer/', views.check_trivia_answer, name='check_trivia_answer'),
    ]