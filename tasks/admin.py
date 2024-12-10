
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'deadline', 'user')
    list_filter = ('priority', 'status', 'deadline')
    search_fields = ('title', 'description')
