from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from Student.models import Student, Admin
from .models import Question, Quiz
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404


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


def home(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Admin/Home.html')
    else:
        return redirect('adminhome')


def Students(request):
    if request.user.is_authenticated and request.user.is_admin:
        students = Student.objects.all()
        return render(request, 'Admin/Students.html', {'students': students})
    else:
        redirect('adminhome')


def Quizes(request):
    if request.user.is_authenticated and request.user.is_admin:
        quizes = Quiz.objects.all()
        return render(request, 'Admin/Quizes.html', {'quizes': quizes})
    else:
        return redirect('adminhome')


class Quiz_detail(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quizobj = Quiz.objects.get(pk=pk)
            print(quizobj.assigned_to)
            questions = Question.objects.filter(quiz=pk)
            question_options = {}
            for question in questions:
                print("Question id:", question.id)
                options = AnswerOptions.objects.filter(question=question)
                option_texts = [option.option_text for option in options]
                question_options[question.id] = option_texts
            print(question_options)
            return render(request, 'Admin/QuizDetails.html', {
                'quiz': quizobj,
                'questions': questions,
                'question_options': question_options,
            })
        else:
            return redirect('adminhome')

    def post(self, request):
        pass


class CreateQuiz(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            quiz_form = QuizForm()
            question_formset = QuestionFormSet(prefix='questions')
            options_formset = AnswerOptionFormSet(prefix='options')
            return render(request, 'Admin/createQuiz.html', {
                'quizform': quiz_form,
                'question_formset': question_formset,
                'options_formset': options_formset
            })
        else:
            return redirect('adminhome')

    def post(self, request):
        # print(request.POST)
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            question_formset = QuestionFormSet(request.POST, instance=quiz, prefix='questions')
            if question_formset.is_valid():
                quiz.save()

                assigned_to_ids = request.POST.getlist('assigned_to')
                assigned_to_students = Student.objects.filter(pk__in=assigned_to_ids)
                quiz.assigned_to.set(assigned_to_students)

                questions = question_formset.save(commit=False)
                for question in questions:
                    question.quiz = quiz
                    question.save()

                    options_formset = AnswerOptionFormSet(request.POST, prefix='options', instance=question)
                    if options_formset.is_valid():
                        options = options_formset.save(commit=False)
                        for option in options:
                            option.question = question
                            option.save()

                return redirect('quizes')

            else:
                return render(request, 'Admin/createQuiz.html', {
                    'quizform': quiz_form,
                    'question_formset': question_formset,
                })
        else:
            return render(request, 'Admin/createQuiz.html', {
                'quizform': quiz_form
            })


class CreateQuestion(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            question_form = QuestionForm()
            formset = AnswerOptionFormSet()
            return render(request, 'Admin/CreateQuestion.html', {'question_form': question_form, 'formset': formset})
        else:
            return redirect('adminhome')

    def post(self, request):
        print(request.POST)
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            quiz = Quiz.objects.get(id=1)
            question.quiz = quiz
            question.save()

            formset = AnswerOptionFormSet(data=self.request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('quizes')
        else:
            return render(
                request,
                'Admin/CreateQuestion.html',
                {'question_form': question_form})

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


class Quiz_Delete(View):
    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = get_object_or_404(Quiz, pk=pk)
            quiz.delete()
            return redirect('quizes')
        else:
            return redirect('adminhome')


# Testing code

class AddOption(TemplateView):
    template_name = "Admin/CreateQuestion.html"

    def get(self, *args, **kwargs):
        formset = AnswerOptionFormSet()
        return self.render_to_response({'formset': formset})

    def post(self, *args, **kwargs):
        formset = AnswerOptionFormSet(data=self.request.POST)
        if formset.is_valid():
            options = formset.save(commit=False)
            for option in options:
                option.question = Question.objects.get(id=1)
                option.save()
            return HttpResponse("Option added successfully")

        return self.render_to_response({'formset': formset})
