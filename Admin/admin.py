from django.contrib import admin
from .models import Admin


class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin')


admin.site.register(Admin, AdminModelAdmin)