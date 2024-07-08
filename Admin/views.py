from django.shortcuts import render, redirect
from Student.models import Student, Admin
from .models import Question, Quiz, AnswerOptions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from .forms import QuestionForm, OptionFormSet, QuizForm, QuestionFormSet


class AdminLogin(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'Admin/AdminLogin.html')
        else:
            return redirect('home')

    def post(self, request):
        error = None
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(email, password)
        admins = Admin.objects.all()
        for admin in admins:
            if admin.email == email and admin.password == password:
                print('hello')
                login(request, admin)
                return redirect('home')

        error = 'Invalid credentials'
        return render(request, 'Admin/AdminLogin.html', {"error": error})



@login_required()
def home(request):
    return render(request, 'Admin/Home.html')


def Students(request):
    if request.user.is_authenticated:
        students = Student.objects.all()
        return render(request, 'Admin/Students.html', {'students': students})
    else:
        redirect('adminhome')


def Quizes(request):
    if request.user.is_authenticated:
        quizes = Quiz.objects.all()
        return render(request, 'Admin/Quizes.html', {'quizes': quizes})
    else:
        return redirect('adminhome')


class Quiz_detail(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            quizobj = Quiz.objects.get(pk=pk)
            questions = Question.objects.all().filter(quiz=pk)
            answer_options = AnswerOptions.objects.all().filter(question=pk)
            return render(request, 'Admin/QuizDetails.html',
                          {'quiz': quizobj,
                           'questions': questions,
                           'options': answer_options
                           })
        else:
            return redirect('adminhome')
    def post(self, request):
        pass


class createQuiz(View):
    def get(self, request):
        if request.user.is_authenticated:
            quizform = QuizForm()
            formset = QuestionFormSet()
            return render(request, 'Admin/CreateQuiz.html', {
                'quizform': quizform,
                'formset': formset
            })
        else:
            return redirect('adminhome')

    def post(self, request):
        quizform = QuizForm(request.POST)
        formset = QuestionFormSet(request.POST)
        questions = Question.objects.all()
        if quizform.is_valid() and formset.is_valid():
            quiz = quizform.save(commit=False)
            formset = QuestionFormSet(request.POST, instance=quiz)
            if formset.is_valid():
                quiz.save()
                formset.save()
                return redirect('quizes')

        return render(request, 'Admin/CreateQuiz.html', {
            'quizform': quizform,
            'formset': formset,
            'questions': questions
        })


class CreateQuestion(View):
    def get(self, request):
        if request.user.is_authenticated:
            question_form = QuestionForm()
            formset = OptionFormSet()
            return render(request, 'Admin/CreateQuestion.html', {'question_form': question_form, 'formset': formset})
        else:
            return redirect('adminhome')

    def post(self, request):
        question_form = QuestionForm(request.POST)
        formset = OptionFormSet(request.POST)
        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()
            formset.instance = question
            formset.save()
            return redirect('createQuiz')  
        return render(request, 'Admin/CreateQuestion.html', {'question_form': question_form, 'formset': formset})

        # ques_type = request.POST.get('question_type')
        # diff_level = request.POST.get('difficulty_level')
        # ques_statement = request.POST.get('question_statement')
        # corr_answer = request.POST.get('correct_answer')
        # ans_choices = request.POST.get('answer_choice')
        #
        # print(ques_statement)
        # print(diff_level)
        # print(ans_choices)
        #
        # ques = Question.objects.create(
        #     question_statement=ques_statement,
        #     question_type=ques_type,
        #     difficulty_level=diff_level,
        #     correct_answer=corr_answer,
        #     answer_choices=ans_choices
        # )
        #
        # return redirect(createQuiz)