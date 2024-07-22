from django.db import models
from Student.models import User


class Admin(User):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
