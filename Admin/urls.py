from django.urls import path
from . views import (
    home, AdminLogin,
    Students, Quizes, CreateQuiz, CreateQuiz2, Quiz_detail, CreateQuestion, Quiz_Delete, UpdateQuiz, UpdateQuestion,
    QuizAttempts, AddOption, UpdateStudent, Student_Delete
)


urlpatterns = [
    path('', AdminLogin.as_view(), name='adminlogin'),
    path('home', home, name='home'),
    path('students/', Students, name='students'),
    path('update_student/<int:pk>/', UpdateStudent.as_view(), name='update_student'),
    path('delete_student/<int:pk>/', Student_Delete.as_view(), name='delete_student'),
    path('quizes/', Quizes, name='quizes'),
    path('createQuiz/', CreateQuiz.as_view(), name='createQuiz'),
    path('createQuiz2/', CreateQuiz2.as_view(), name='createQuiz2'),
    path('quiz/<int:pk>/', Quiz_detail.as_view(), name='quiz_detail'),
    path('createQuestion/<int:pk>/', CreateQuestion.as_view(), name='createQuestion'),
    path('quiz/<int:pk>/delete/', Quiz_Delete.as_view(), name='quiz_delete'),
    path('updatequiz/<int:pk>/', UpdateQuiz.as_view(), name='updateQuiz'),
    path('updatequestion/<int:pk>/', UpdateQuestion.as_view(), name='updateQuestion'),
    path('quizattempts/<int:pk>/', QuizAttempts.as_view(), name='quizattempts'),

    # path('createQuestion/', AddOption.as_view(), name="createQuestion")
]
