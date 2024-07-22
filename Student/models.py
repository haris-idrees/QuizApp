from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Student(User):
    phone_number = models.CharField(max_length=11, blank=True, default= "")
    enrollment_number = models.CharField(max_length=10, default= "")

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
