from .models import *
from rest_framework import serializers


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id','username', 'email', 'password', 'is_admin']

