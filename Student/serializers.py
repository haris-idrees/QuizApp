from .models import Student
from rest_framework import serializers
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','username', 'email', 'password', 'phone_number', 'enrollment_number', 'is_student']

