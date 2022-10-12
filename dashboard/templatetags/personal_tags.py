from datetime import datetime
from django.db.models import Q
from django import template
from django.contrib.auth.models import User, Group
from django_currentuser.middleware import get_current_user

from accounts.models import Profile
from reference_books.models import StatusTask
from tasks.models import Tasks

__author__ = 'ipman'
register = template.Library()


@register.filter
def view_shortfio_user(user):
    try:
        return get_shortfio(user.last_name+' '+user.first_name)
    except:
        return 'ошибка'


@register.filter
def view_shortfio_user(login):
    try:
        user = User.objects.get(username=login)
        return get_shortfio(user.last_name+' '+user.first_name)
    except:
        return 'ошибка'


@register.filter
def get_gender(user):
    try:
        return Profile.objects.get(user=user).gender
    except:
        return 'ошибка'


@register.filter
def get_shortfio(fio):
    if fio:
        split_fio = fio.split(' ')
        if len(split_fio) == 1:
            return split_fio
        elif len(split_fio) == 2:
            return split_fio[0]+' '+split_fio[1][:1]+'.'
        elif len(split_fio) == 3:
            return split_fio[0]+' '+split_fio[1][:1]+'.'+split_fio[2][:1]+'.'
        else:
            return 'неизвестно'
    else:
        return 'нет'


@register.inclusion_tag('templatetags/notify.html')
def notify_topbar():
    cur_user = get_current_user()
    tasks = Tasks.objects.filter(Q(executor=Profile.objects.get(user=cur_user), status__in=StatusTask.objects.all())|
                                 Q(group_executor__in=cur_user.groups.all()), read=False)
    return {'tasks': tasks.order_by('-id')[:10], 'cur_date': datetime.today().date(), 'all_notify_count': tasks.count()}
