from django.urls import path, include
from . views import home, AdminLogin, Students, Quizes, createQuiz, CreateQuestion, Quiz_detail
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', AdminLogin.as_view(), name='adminhome'),
    path('home', home, name='home'),
    path('students/', Students, name='students'),
    path('quizes/', Quizes, name='quizes'),
    path('createQuiz/', createQuiz.as_view(), name='createQuiz'),
    path('quiz/<int:pk>/', Quiz_detail.as_view(), name='quiz_detail'),
    path('createQuestion/', CreateQuestion.as_view(), name='creatQuestion')
]
