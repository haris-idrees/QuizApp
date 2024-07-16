from django.urls import path
from . views import (
    home,
    AdminLogin,
    Students, Quizes, CreateQuiz, Quiz_detail, CreateQuestion, Quiz_Delete,
    AddOption)


urlpatterns = [
    path('', AdminLogin.as_view(), name='adminhome'),
    path('home', home, name='home'),
    path('students/', Students, name='students'),
    path('quizes/', Quizes, name='quizes'),
    path('createQuiz/', CreateQuiz.as_view(), name='createQuiz'),
    path('quiz/<int:pk>/', Quiz_detail.as_view(), name='quiz_detail'),
    path('createQuestion/', CreateQuestion.as_view(), name='creatQuestion'),
    path('quiz/<int:pk>/delete/', Quiz_Delete.as_view(), name='quiz_delete'),
    # path('createQuestion/', AddOption.as_view(), name="createQuestion")
]
