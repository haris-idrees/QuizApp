from .models import Student, Admin
from rest_framework import serializers
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','username', 'email', 'password', 'phone_number', 'enrollment_number', 'is_student']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id','username', 'email', 'password', 'is_admin']

