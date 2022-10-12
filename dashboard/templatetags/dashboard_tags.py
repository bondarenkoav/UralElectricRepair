__author__ = 'ipman'

from datetime import datetime
from django import template

from dashboard.models import Menu

register = template.Library()


# Вывод текущего года на странице Авторизации
@register.simple_tag
def current_year():
    return datetime.today().year


# Вывод текущего года на странице Авторизации
@register.simple_tag
def get_today():
    return datetime.today().date()


@register.inclusion_tag('templatetags/sidebar_menu.html')
def tag_navigation():
    return {'nodes': Menu.objects.all()}


@register.simple_tag
def current_user(request):
    return request.user.first_name + ' ' + request.user.last_name
