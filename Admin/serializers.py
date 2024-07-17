from .models import *
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        fields = '__all__'


class StudentQuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentQuizAttempt
        fields = '__all__'


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'
