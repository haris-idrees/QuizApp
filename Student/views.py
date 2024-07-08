from django.shortcuts import render, redirect
from django.http import HttpResponse
from .serializers import StudentSerializer, AdminSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Student, Admin
from rest_framework import viewsets
from django.views import View
from django.contrib.auth.decorators import login_required
from Admin.models import Question, Quiz, AnswerOptions
from Admin.serializers import QuestionSerializer, QuizSerializer, OptionSerializer


def home(request):
    return render(request, 'Student/home.html')


class RegisterStudent(View):
    def get(self, request):
        return render(request, 'Student/RegisterStudent.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('number')
        enrollment_id = request.POST.get('enroll')

        error = None
        if not email or not password:
            error = 'Plz enter values for email and password'
            return render(request, 'Student/RegisterStudent.html', {'error': error})

        elif Student.objects.filter(username=username).exists():
            error = 'Username already exists. Please choose a different username.'
            return render(request, 'Student/RegisterStudent.html', {'error': error})

        elif len(phone) < 11 or not phone.isdigit():
            error = 'Enter a valid number'
            return render(request, 'Student/RegisterStudent.html', {'error': error})

        std = Student.objects.create(
            username=username,
            email=email,
            password=password,
            phone_number=phone,
            enrollment_number=enrollment_id
        )

        return render(request, 'Student/LoginStudent.html')


class LoginStudent(View):
    def get(self, request):
        return render(request, 'Student/LoginStudent.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        students = Student.objects.all()
        for std in students:
            if std.password == password and std.username == username:
                print(username, password)
                login(request, std)
                request.session['username'] = username
                request.session.save()
                return redirect(Profile)

        error = 'Invalid credentials'
        return render(request, 'Student/LoginStudent.html', {'error': error})


def logout_student(request):
    logout(request)
    return redirect('login_student')


@login_required()
def Profile(request):
    username = request.session.get('username')
    student = Student.objects.get(username=username)
    assigned_quizes = Quiz.objects.all().filter(assigned_to=student)
    return render(request, 'Student/Profile.html', {'student': student, 'quizes': assigned_quizes})


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOptions.objects.all()
    serializer_class = OptionSerializer
