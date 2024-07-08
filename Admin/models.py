from django.db import models
from Student.models import Student
from django.contrib.auth.models import User


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
    correct_answer = models.CharField(max_length=512)

    def __str__(self):
        return self.question_statement


class AnswerOptions(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length= 256)

    def __str__(self):
        return self.option_text
