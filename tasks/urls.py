from django.conf.urls import url

from tasks.views import getlist_tasks, getitem_task, planning, getlist_archive_tasks

__author__ = 'ipman'

app_name = 'tasks'

urlpatterns = [
    url(r'^task-(?P<pk>\d+)/$', getitem_task, name='getitem-task'),

    url(r'^planning/$', planning, name='planning'),
    # Вывод архива
    url(r'^archive/$', getlist_archive_tasks, name='getlist-archive-tasks'),
    # Вывод не выполненых задач
    url(r'^', getlist_tasks, name='getlist-tasks'),
]