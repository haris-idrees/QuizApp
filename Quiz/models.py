from django.db import models
from Student.models import Student


class Quiz(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    title = models.CharField(max_length=100)
    # questions = models.ManyToManyField(Question)
    assigned_to = models.ManyToManyField(Student)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="")
    Total_score = models.IntegerField(default=10, blank=True)
    Time_allowed = models.IntegerField(help_text="Enter duration in minutes")

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_types = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer')
    )
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    question_statement = models.CharField(max_length=256)
    question_type = models.CharField(max_length=10, choices=question_types)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    correct_answer = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.question_statement


class AnswerOptions(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length= 256)

    def __str__(self):
        return self.option_text


class StudentQuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(auto_now_add=True)
    attempt_score = models.IntegerField()

    class Meta:
        unique_together = ('student', 'quiz')

    def __str__(self):
        return f'{self.student} - {self.quiz}'


class StudentAnswer(models.Model):
    attempt = models.ForeignKey(StudentQuizAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return f'{self.attempt.student} - {self.question} - {self.answer}'

