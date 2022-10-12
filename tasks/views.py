import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django_currentuser.middleware import get_current_user

from accounts.models import Profile
from reference_books.models import StatusTask, TreeTechProcess
from tasks.forms import KanbanForm, TasksArchiveForm
from tasks.models import Tasks

__author__ = 'ipman'

content_area = u'Рабочий стол'
logger = logging.getLogger(__name__)


@login_required
def getlist_tasks(request):
    cur_user = get_current_user()
    tasks = Tasks.objects.filter(Q(executor=Profile.objects.get(user=cur_user)) |
                                 Q(group_executor__in=cur_user.groups.all()) |
                                 Q(author=Profile.objects.get(user=cur_user)), complete=False)\
        .order_by('-datetime_update')

    return render(request, 'tasks/tasks_list.html', {
        'title': 'Задачи',
        'tasks': tasks,
    })


@login_required
def getlist_archive_tasks(request):
    archive = []
    cur_user = get_current_user()
    form = TasksArchiveForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            start_period = form.cleaned_data['start_period']
            end_period = form.cleaned_data['end_period']

            archive = Tasks.objects.\
                filter(Q(executor=Profile.objects.get(user=cur_user)) |
                       Q(group_executor__in=cur_user.groups.all()) |
                       Q(author=Profile.objects.get(user=cur_user)),
                       complete=True, datetime_update__range=(start_period, end_period)).order_by('-datetime_update')

    return render(request, 'tasks/tasks_archive_list.html', {
        'title': 'Архив задач',
        'archive': archive,
        'form_archive': form
    })


@login_required
@csrf_protect
def getitem_task(request, pk):
    Tasks.objects.filter(id=pk).update(read=True)
    if Tasks.objects.get(id=pk).task_name == 'verificationpassed':
        Tasks.objects.filter(id=pk).update(complete=True)
    task_data = Tasks.objects.get(id=pk)
    return render(request, 'tasks/tasks_item.html', {
        'title': 'Задача',
        'task_data': task_data,
    })


# Нужно назначить исполнителя
def add_task_assignperformer(app_name, model_name, fun_name, record_pk, sc_pk, name, title, curr_user, receiving, date_due):
    if Tasks.objects.filter(model_name=model_name, task_name=fun_name, record_id=record_pk).count() == 0:
        group = executor = None
        if receiving.user.username == 'otk':
            group = Group.objects.get(name='ОТК')
        else:
            executor = receiving
        Tasks.objects.create(app_name=app_name, model_name=model_name, task_name=fun_name, record_id=record_pk,
                             path=reverse('production:assign-performer', kwargs={'type': model_name, 'pk': record_pk}),
                             scopeshipment_id=sc_pk, title=title, description=name, author=Profile.objects.get(user=curr_user),
                             group_executor=group, executor=executor, date_limit=date_due,
                             status=StatusTask.objects.get(slug='assign_performer'))


# Если исполнитель назначен или назначается начальником участка
def add_task_appointedperformer(app_name, model_name, fun_name, record_pk, sc_pk, _url, name, title, curr_user, executor, date_due):
    if Tasks.objects.filter(model_name=model_name, task_name=fun_name, record_id=record_pk, executor=executor).count() == 0:
        Tasks.objects.create(app_name=app_name, model_name=model_name, task_name=fun_name, record_id=record_pk,
                             scopeshipment_id=sc_pk, path=reverse(_url, kwargs={'pk': record_pk}),
                             title=title, description=name, author=Profile.objects.get(user=curr_user),
                             executor=executor, date_limit=date_due,
                             status=StatusTask.objects.get(slug='appointed_performer'))


# Сообщение проверяющему
def add_task_forchecking(app_name, model_name, fun_name, record_pk, sc_pk, _url, name, title, curr_user, receiving):
    if Tasks.objects.filter(model_name=model_name, task_name=fun_name, record_id=record_pk).count() == 0:
        group = executor = None
        if receiving.user.username == 'otk':
            group = Group.objects.get(name='ОТК')
        else:
            executor = receiving
        Tasks.objects.create(app_name=app_name, model_name=model_name, task_name=fun_name, record_id=record_pk,
                             scopeshipment_id=sc_pk, path=reverse(_url, kwargs={'pk': record_pk}), title=title,
                             description=name, author=Profile.objects.get(user=curr_user),
                             status=StatusTask.objects.get(slug='forchecking'), group_executor=group, executor=executor)


# Если проверку прошел
def add_task_verificationpassed(app_name, model_name, fun_name, sc_pk, record_pk, name, title, curr_user):
    if Tasks.objects.filter(model_name=model_name, task_name=fun_name, record_id=record_pk).count() == 0:
        Tasks.objects.create(app_name=app_name, model_name=model_name, task_name=fun_name, record_id=record_pk,
                             scopeshipment_id=sc_pk, path=reverse('production:scopeshipment-update', kwargs={'pk': sc_pk}),
                             title=title, description=name, author=Profile.objects.get(user=curr_user),
                             group_executor=Group.objects.get(name='ИТР'))


def update_task_complete(app_name, model_name, fun_name, record_pk):
    Tasks.objects.filter(app_name=app_name, model_name=model_name, task_name=fun_name,
                         record_id=record_pk, complete=False).update(complete=True)


@login_required
def planning(request):
    root_parent_nodes = TreeTechProcess.objects.filter(parent__isnull=True)
    form = KanbanForm(request.POST or None)
    # all_tasks = Task.query.all()
    # result = tasks_schema.dump(all_tasks).data
    #
    # to_do = []
    # doing = []
    # done = []
    #
    # for i in result:
    #     if datetime.strptime(i['completedate'][:10], '%Y-%m-%d') > datetime.today():
    #         i['overdue'] = False
    #     else:
    #         i['overdue'] = True
    #     if i['category'] == 'To Do':
    #         to_do.append(i)
    #     elif i['category'] == 'Doing':
    #         doing.append(i)
    #     else:
    #         done.append(i)
    #
    # to_do.sort(key=lambda r: r['completedate'])
    # doing.sort(key=lambda r: r['completedate'])
    # done.sort(key=lambda r: r['completedate'])
    #
    return render(request, 'tasks/planning.html', {
        'root_parent_nodes': root_parent_nodes,
        'form': form
        # 'update_todo': to_do,
        # 'update_doing': doing,
        # 'update_done': done
    })


@login_required
def planning_update(request):
    pass


@login_required
def planning_move(request):
    pass
