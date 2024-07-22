from django.contrib import admin
from .models import Student


class StudentModel(admin.ModelAdmin):
    list_display = ('username', 'email', 'enrollment_number', 'phone_number', 'is_student')


admin.site.register(Student, StudentModel)
