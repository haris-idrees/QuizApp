from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Student.models import Student
from .serializers import StudentSerializer
from django.contrib.auth import login, logout
from Quiz.models import Quiz, Question, StudentQuizAttempt, StudentAnswer, AnswerOptions
from rest_framework import viewsets
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import transaction
from django.conf import settings


def home(request):
    return render(request, 'Student/home.html')


class RegisterStudent(View):
    def get(self, request):
        return render(request, 'Student/RegisterStudent.html')

    @transaction.atomic
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
            enrollment_number=enrollment_id,
            is_student=True
        )

        return render(request, 'Student/LoginStudent.html')


class LoginStudent(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'Student/LoginStudent.html')
        else:
            return redirect('home')


    @transaction.atomic
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
                return redirect('profile' , pk=std.pk)

        error = 'Invalid credentials'
        return render(request, 'Student/LoginStudent.html', {'error': error})


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'Student/forgotpassword.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            student = Student.objects.get(email=email)
            if student:
                context = {
                    'protocol': 'http',
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(student.pk)),
                    'token': default_token_generator.make_token(student)
                }
                html_content = render_to_string('Student/password_reset_email.html', context)
                text_content = strip_tags(html_content)

                email = EmailMessage(
                    subject='Reset Password',
                    body=text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                email.content_subtype = 'html'

                email.send()

                return render(request, 'Student/EmailConfirmation.html')

        except Exception as e:
            error = 'You are not a registered User'
            return render(request, 'Student/RegisterStudent.html', {'error': error})

        # subject = 'Password Reset'
        # message = 'Your password has been reset'
        # if subject and message:
        #     try:
        #         send_mail(
        #             subject,
        #             message,
        #             settings.EMAIL_HOST_USER,
        #             ["harisidrees135@gmail.com"],
        #             fail_silently=False
        #         )
        #     except BadHeaderError:
        #         return HttpResponse("Invalid header found.")
        #     except Exception as e:
        #         print(f"Failed to send email: {e}")
        #         return HttpResponse("Failed to send email.")
        #
        #     return HttpResponse("Email sent")
        # else:
        #     return HttpResponse("Make sure all fields are entered and valid.")


class EmailConfirmation(View):
    def get(self, request):
        return render(request, 'Student/EmailConfirmation.html')

    def post(self, request):
        pass


class SetPassword(View):
    def get(self, request, uidb64, token):
        return render(request, 'Student/setpassword.html')

    def post(self, request, uidb64, token):
        password = request.POST.get('password')
        print(password)
        uid = force_str(urlsafe_base64_decode(uidb64))
        student = Student.objects.get(pk=uid)
        student.set_password(password)
        student.save()
        return render(request, 'Student/ResetSuccess.html')


class ResetSuccess(View):
    def get(self, request):
        return render(request, 'Student/ResetSuccess.html')


def logout_student(request):
    logout(request)
    return redirect('login_student')


class Profile(View):
    def get(self, request, pk):
        if request.user.is_authenticated and request.user.is_student:
            student = Student.objects.get(pk=pk)

            assigned_quizes = Quiz.objects.all().filter(assigned_to=student)

            attempts = StudentQuizAttempt.objects.filter(student=student)
            attempted_quizes = []
            for attempt in attempts:
                attempted_quizes.append(attempt.quiz)

            unattempted_quizes = []
            for quiz in assigned_quizes:
                if quiz not in attempted_quizes:
                    unattempted_quizes.append(quiz)

            return render(request, 'Student/Profile.html',{
                           'student': student,
                           'attempts': attempts,
                           'unattempted_quizes': unattempted_quizes
            })
    def post(self, request, pk):
        pass


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
            return redirect('profile', pk=request.user.id)

    @transaction.atomic
    def post(self, request, pk):
        if request.user.is_authenticated and request.user.is_student:
            quizobj = Quiz.objects.get(pk=pk)

            attempt_exists = StudentQuizAttempt.objects.filter(student=request.user, quiz=quizobj).exists()
            if attempt_exists:
                return HttpResponse("You have already attempted this Quiz")

            student = Student.objects.get(pk=request.user.id)
            attempt = StudentQuizAttempt.objects.create(student=student, quiz=quizobj, attempt_score=0)

            questions = Question.objects.filter(quiz=quizobj)
            attempt_score = 0
            for question in questions:
                answer = request.POST.get(f'answer_{question.id}')
                if answer:
                    if answer == question.correct_answer:
                        attempt_score += 1
                        StudentAnswer.objects.create(
                            attempt=attempt,
                            question=question,
                            answer=answer,
                            score=1
                        )
                    else:
                        StudentAnswer.objects.create(
                            attempt=attempt,
                            question=question,
                            answer=answer,
                            score=0
                        )
            attempt.attempt_score = attempt_score
            attempt.save()
            return redirect('profile', pk=request.user.id)
        else:
            return redirect('home')


class ViewAttempt(View):
    def get(self, request, quiz_id):
        if request.user.is_authenticated and request.user.is_student:
            student = Student.objects.get(id=request.user.id)
            quiz = Quiz.objects.get(pk=quiz_id)
            attempt = StudentQuizAttempt.objects.get(student=student, quiz=quiz)
            answers = StudentAnswer.objects.filter(attempt=attempt)
            questions = Question.objects.filter(quiz=quiz)
            question_options = {question.id: AnswerOptions.objects.filter(question=question) for question in questions}
            return render(request, 'Student/ViewAttempt.html', {
                'student': student,
                'quiz': quiz,
                'attempt': attempt,
                'questions': questions,
                'question_options': question_options,
                'attempted_answers': answers,
            })


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

