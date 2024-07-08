from .models import Student, Admin
from rest_framework import serializers
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'phone_number', 'enrollment_number']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password']

