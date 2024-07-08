from django.urls import path, include
from . views import (home,
                     StudentViewSet,
                     RegisterStudent,
                     LoginStudent,
                     Profile,
                     AdminViewSet,
                     logout_student,
                     QuizViewSet,
                     QuestionViewSet,
                     OptionViewSet
                     )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('student', StudentViewSet , basename='student')
router.register('admin', AdminViewSet, basename='admin')
router.register('question', QuestionViewSet, basename='question')
router.register('quiz', QuizViewSet, basename='quiz')
router.register('options', OptionViewSet, basename='options')

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginStudent.as_view(), name='login_student'),
    path('profile/', Profile, name='profile'),
    path('logout/', logout_student, name='logout'),
    path('api/', include(router.urls))
]
