# -*- coding: utf-8 -*-
import os

from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from django_currentuser.db.models import CurrentUserField

from accounts.models import Profile
from reference_books.models import TypeNotificationTask, StatusTask


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Файл не поддерживается.')


def task_file_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "task_id%s.%s" % (str(instance.id), ext)
    return os.path.join('tasks/', filename)


TypeTasks = (
    ('repairfund', 'Ремонтный фонд'),
    ('other', 'Другое'),
)


class Tasks(models.Model):
    title = models.CharField(u'Заголовок задачи', max_length=100)
    description = models.TextField(u'Описание задачи')
    author = models.ForeignKey(Profile, verbose_name=u'Назначающий', related_name='author', on_delete=models.CASCADE)

    group_executor = models.ForeignKey(Group, models.SET_NULL, null=True, verbose_name=u'Группа исполнителей',
                                       related_name='group_executor')
    executor = models.ForeignKey(Profile, models.SET_NULL, null=True, verbose_name=u'Исполнитель',
                                 related_name='executor')
    date_limit = models.DateField(u'Дата исполнения', blank=True, null=True)
    high_importance = models.BooleanField(u'Высокая важность', default=False)

    app_name = models.CharField(u'Приложение', choices=TypeTasks, max_length=30)
    model_name = models.CharField(u'Имя модели', max_length=50, blank=True, null=True)
    task_name = models.CharField(u'Имя задачи', max_length=50, blank=True, null=True)
    record_id = models.IntegerField(u'ID задачи', blank=True, null=True)
    scopeshipment_id = models.IntegerField(u'Оборудование', blank=True, null=True)

    path = models.URLField(max_length=200, blank=True, null=True)
    notification = models.ForeignKey(TypeNotificationTask, models.SET_NULL, null=True,
                                     verbose_name=u'Способ уведомления о статусе заявки')
    status = models.ForeignKey(StatusTask, models.SET_NULL, null=True, verbose_name=u'Тип задачи')
    work_desc = models.TextField(u'Описание выполнения', blank=True, null=True)
    read = models.BooleanField(u'Прочтено', default=False)
    complete = models.BooleanField(u'Выполнено', default=False)
    file = models.FileField(blank=True, null=True, validators=[validate_file_extension], upload_to=task_file_rename)

    create_user = models.ForeignKey(User, models.SET_NULL, null=True,
                                    verbose_name=u'Создал', related_name='create_user')
    update_user = models.ForeignKey(User, models.SET_NULL, null=True,
                                    verbose_name=u'Обновил', related_name='update_user', blank=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Задача '
        verbose_name_plural = u'Список задач '


class Kanban(models.Model):
    author = models.ForeignKey(Profile, verbose_name=u'Назначающий', related_name='kw_author', on_delete=models.CASCADE)

    curr_week = models.DateField(u'Начало недели', blank=True, null=True)
    curr_day = models.DateField(u'День', blank=True, null=True)

    model_name = models.CharField(u'Имя модели', max_length=50, blank=True, null=True)
    record_pk = models.IntegerField(u'ИД модели', blank=True, null=True)

    create_user = CurrentUserField(related_name='kw_create_user', on_update=False)
    update_user = CurrentUserField(related_name='kw_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return 'План на ' + self.curr_week.strftime("%V") + ' неделю ' + self.curr_day.__str__()

    class Meta:
        verbose_name = u'Неделя '
        verbose_name_plural = u'План на неделю '
