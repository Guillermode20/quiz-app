from django.urls import path
from . import views

urlpatterns = [
    path('trivia_restart/', views.trivia_restart, name='restart'),
    path('', views.startpage, name='startpage'),
    path('trivia/', views.get_trivia_questions, name='trivia'),
    path('check_trivia_answer/', views.check_trivia_answer, name='check_trivia_answer'),
    path('stats', views.stats, name='stats'),
    ]