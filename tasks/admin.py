from django.contrib import admin

from tasks.models import Tasks


class TasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'executor', 'datetime_add', 'read']
    list_filter = ['author', 'executor', 'datetime_add']
    model = Tasks


admin.site.register(Tasks, TasksAdmin)