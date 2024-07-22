from django.db import transaction
from django.shortcuts import render, redirect
from Student.models import Student
from .models import Admin
from .serializers import AdminSerializer
from Quiz.models import Question, Quiz, StudentQuizAttempt, AnswerOptions, StudentAnswer
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse
from Quiz.forms import *
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class AdminLogin(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'Admin/AdminLogin.html')
        elif request.user.is_student and request.user.is_authenticated:
            return render(request, 'Student/home.html')
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
        return redirect('adminlogin')


def Students(request):
    if request.user.is_authenticated and request.user.is_admin:
        students = Student.objects.all()
        return render(request, 'Admin/Students.html', {'students': students})
    else:
        redirect('adminlogin')


def Quizes(request):
    if request.user.is_authenticated and request.user.is_admin:
        quizes = Quiz.objects.all()
        return render(request, 'Admin/Quizes.html', {'quizes': quizes})
    else:
        return redirect('adminlogin')


class Quiz_detail(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quizobj = Quiz.objects.get(pk=pk)
            print(quizobj.assigned_to)
            questions = Question.objects.filter(quiz=pk)
            assigned_students = quizobj.assigned_to.all()
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
                'assigned_students': assigned_students,
            })
        else:
            return redirect('adminlogin')

    def post(self, request):
        pass


class CreateQuiz(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            quiz_form = QuizForm()
            question_formset = QuestionFormSet(prefix='questions')
            options_formset = AnswerOptionFormSet(prefix='options')
            return render(request, 'Admin/CreateQuiz.html', {
                'quizform': quiz_form,
                'question_formset': question_formset,
                'options_formset': options_formset
            })
        else:
            return redirect('adminlogin')

    @transaction.atomic()
    def post(self, request):
        print(request.POST)
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
                question_len = 0
                ques_num = 0
                for question in questions:
                    question_len += 1
                    question.quiz = quiz
                    question.save()

                    option_texts = request.POST.getlist(f'questions-{ques_num}-option_text')

                    if question.correct_answer not in option_texts:
                        return render(request, 'Admin/CreateQuiz.html', {
                            'quizform': quiz_form,
                            'question_formset': question_formset,
                            'options': option_texts
                        })
                    else:
                        for option_text in option_texts:
                            answer_options = AnswerOptions.objects.create(question=question, option_text=option_text)

                    ques_num += 1


                quiz.Total_score = question_len
                quiz.save()
                return redirect('quizes')

            else:
                return render(request, 'Admin/CreateQuiz.html', {
                    'quizform': quiz_form,
                    'question_formset': question_formset,
                })
        else:
            return render(request, 'Admin/createQuiz.html', {
                'quizform': quiz_form
            })


class CreateQuiz2(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            quiz_form = QuizForm(request.POST)
            formset = QuestionFormSet(prefix='questions')
            questions = Question.objects.all()
            return render(request, 'Admin/CreateQuiz2.html', {
                'quizform': quiz_form,
                'formset': formset,
                'questions': questions
            })

    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = QuizForm(request.POST)
            formset = QuestionFormSet(request.POST, instance=quiz)


class UpdateQuiz(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = Quiz.objects.get(pk=pk)
            quiz_form = QuizForm(instance=quiz)
            questions = Question.objects.filter(quiz=quiz)
            return render(request, 'Admin/UpdateQuiz.html', {
                'quizid': pk,
                'quizform': quiz_form,
                'questions': questions,
            })

    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = Quiz.objects.get(pk=pk)
            quiz_form = QuizForm(request.POST, instance=quiz)

            if quiz_form.is_valid():
                quiz_form.save(commit=False)

                checked_question_ids = request.POST.getlist('question_ids')
                print(checked_question_ids)
                checked_question_ids = [int(id) for id in checked_question_ids]

                all_questions = Question.objects.filter(quiz=quiz)
                for question in all_questions:
                    if question.id not in checked_question_ids:
                        question.delete()

                questions = Question.objects.filter(quiz=quiz)
                total_score = len(questions)
                print("New Total score", total_score)
                quiz.Total_score = total_score

                assigned_to_ids = request.POST.getlist('assigned_to')
                assigned_to = Student.objects.filter(id__in=assigned_to_ids)
                quiz.assigned_to.set(assigned_to)

                quiz.save()

                return redirect('quiz_detail', pk=pk)

        return render(request, 'Admin/UpdateQuiz.html', {
            'quizid': pk,
            'quizform': quiz_form,
            'questions': Question.objects.filter(quiz=pk),
        })


class UpdateQuestion(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            question = Question.objects.get(pk=pk)
            question_form = QuestionForm(instance=question)
            option_formset = AnswerOptionFormSet(instance=question)
            return render(request, 'Admin/UpdateQuestion.html', {
                'question_form': question_form,
                'formset': option_formset
            })

    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            question = Question.objects.get(pk=pk)
            question_form = QuestionForm(request.POST, instance=question)
            option_formset = AnswerOptionFormSet(request.POST, instance=question)

            if question_form.is_valid() and option_formset.is_valid():
                question_form.save()
                option_formset.save()

                quiz = Quiz.objects.get(pk=question.quiz_id)
                return redirect('quiz_detail', pk=quiz.id)
            else:
                return render(request, 'Admin/UpdateQuestion.html', {
                    'question_form': question_form,
                    'formset': option_formset
                })
        else:
            return redirect('adminlogin')


class CreateQuestion(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            question_form = QuestionForm()
            formset = AnswerOptionFormSet()
            return render(request, 'Admin/CreateQuestion.html', {'question_form': question_form, 'formset': formset})
        else:
            return redirect('adminlogin')

    @transaction.atomic
    def post(self, request,pk):
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            quiz = Quiz.objects.get(pk=pk)
            question.quiz = quiz
            question.save()

            formset = AnswerOptionFormSet(data=self.request.POST, instance=question)
            if formset.is_valid():
                options = formset.save(commit=False)
                option_texts = []
                for option in options:
                    option_texts.append(option.option_text)
                if question.correct_answer:
                    if question.correct_answer not in option_texts:
                        return render(request, 'Admin/CreateQuestion.html', {
                            'question_form': question_form,
                            'formset': formset,
                            'error': "The answer options should include the Correct Answer"
                        })
                formset.save()
                return redirect('updateQuiz', pk=pk)
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


class QuizAttempts(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = Quiz.objects.get(pk=pk)
            attempts = StudentQuizAttempt.objects.filter(quiz=quiz)
            best_attempt = attempts.first()
            if best_attempt:
                top_scorer = best_attempt.student
                if attempts:
                    for attempt in attempts:
                        if attempt.attempt_score > best_attempt.attempt_score:
                            best_attempt = attempt
                    top_scorer = best_attempt.student
                return render(request, 'Admin/QuizAttempts.html', {
                    'quiz': quiz,
                    'topper': top_scorer,
                    'attempts': attempts,
                })
            else:
                return render(request, 'Admin/QuizAttempts.html', {
                    'quiz': quiz,
                    'attempts': attempts,
                })
        else:
            return redirect('quizes')

    def post(self, request, pk):
        pass


class Quiz_Delete(View):
    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            quiz = get_object_or_404(Quiz, pk=pk)
            quiz.delete()
            return redirect('quizes')
        else:
            return redirect('adminlogin')


class UpdateStudent(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            student = Student.objects.get(pk=pk)

            return render(request, 'Admin/UpdateStudent.html', {'student': student})

    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            student = Student.objects.get(pk=pk)

            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('number')
            enrollment_id = request.POST.get('enroll')

            error = None
            if not email:
                error = 'Plz enter values for email and password'
                return render(request, 'Student/RegisterStudent.html', {'error': error})

            elif username != student.username:
                if Student.objects.filter(username=username).exists() or Admin.objects.filter(username=username).exists():
                    error = 'Username already taken'
                    return render(request, 'Admin/UpdateStudent.html', {
                        'student': student,
                        'error': error
                    })

            elif len(phone) < 11 or not phone.isdigit():
                error = 'Enter a valid number'
                return render(request, 'Admin/UpdateStudent.html', {
                    'student': student,
                    'error': error
                })

            student.username = username
            student.email = email
            student.phone_number = phone
            student.enrollment = enrollment_id
            student.save()

            return redirect('students')
        else:
            return redirect('adminlogin')


class Student_Delete(View):
    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_admin:
            student = Student.objects.get(pk=pk)
            student.delete()
            return redirect('students')
        else:
            return redirect('adminlogin')

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
