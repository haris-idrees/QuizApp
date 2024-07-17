from django.shortcuts import render, redirect
from django.http import HttpResponse
from .serializers import StudentSerializer, AdminSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Student, Admin
from rest_framework import viewsets
from django.views import View
from django.contrib.auth.decorators import login_required
from Admin.models import Question, Quiz, AnswerOptions, StudentAnswer, StudentQuizAttempt
from Admin.serializers import *


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


class AttemptQuiz(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_student:
            quizobj = Quiz.objects.get(pk=pk)
            print(quizobj.assigned_to)

            attempt_exists = StudentQuizAttempt.objects.filter(student=request.user, quiz=quizobj).exists()
            if attempt_exists:
                return HttpResponse('You have already attempted this Quiz')

            questions = Question.objects.filter(quiz=pk)
            question_options = {}
            for question in questions:
                print("Question id:", question.id)
                options = AnswerOptions.objects.filter(question=question)
                option_texts = [option.option_text for option in options]
                question_options[question.id] = option_texts
            print(question_options)
            return render(request, 'Student/AttemptQuiz.html', {
                'quiz': quizobj,
                'questions': questions,
                'question_options': question_options,
            })
        else:
            return redirect('adminhome')

    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_student:
            quizobj = Quiz.objects.get(pk=pk)

            attempt_exists = StudentQuizAttempt.objects.filter(student=request.user, quiz=quizobj).exists()
            if attempt_exists:
                return HttpResponse("You have already attempted this Quiz")

            student = Student.objects.get(pk=request.user.id)
            attempt = StudentQuizAttempt.objects.create(student=student, quiz=quizobj)

            questions = Question.objects.filter(quiz=quizobj)
            for question in questions:
                answer = request.POST.get(f'answer_{question.id}')
                if answer:
                    StudentAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        answer=answer
                    )
            return redirect('profile')
        else:
            return redirect('home')


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


class StudentAttemptViewSet(viewsets.ModelViewSet):
    queryset = StudentQuizAttempt.objects.all()
    serializer_class = StudentQuizAttemptSerializer


class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
