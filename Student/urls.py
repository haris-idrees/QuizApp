from django.urls import path, include
from . views import (home,
                     StudentViewSet, RegisterStudent, LoginStudent, Profile,
                     logout_student, ForgotPassword,
                     EmailConfirmation, SetPassword, ResetSuccess, AttemptQuiz, ViewAttempt
                     )
from Quiz.views import QuizViewSet, QuestionViewSet, StudentAttemptViewSet,OptionViewSet,StudentAnswerViewSet
from Admin.views import AdminViewSet

from Admin.views import AdminLogin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('student', StudentViewSet , basename='student')
router.register('admin', AdminViewSet, basename='admin')
router.register('question', QuestionViewSet, basename='question')
router.register('quiz', QuizViewSet, basename='quiz')
router.register('options', OptionViewSet, basename='options')
router.register('attempts', StudentAttemptViewSet, basename='attempts')
router.register('answers', StudentAnswerViewSet, basename='answers')

urlpatterns = [
    path('', home, name='home'),
    path('adminlogin/', AdminLogin.as_view(), name='manager'),
    path('register/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginStudent.as_view(), name='login_student'),
    path('profile/<int:pk>', Profile.as_view(), name='profile'),
    path('logout/', logout_student, name='logout'),
    # path('manager/', home, name='manager'),
    path('AttemptQuiz/<int:pk>/', AttemptQuiz.as_view(), name='AttemptQuiz'),
    path('ViewAttempt/<int:quiz_id>', ViewAttempt.as_view(), name='view_attempt'),
    path('password_reset/', ForgotPassword.as_view(), name='forgot_password'),
    path('password_reset_done/', EmailConfirmation.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', SetPassword.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', ResetSuccess.as_view(), name='password_reset_complete'),

    path('api/', include(router.urls))
]
