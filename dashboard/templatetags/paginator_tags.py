__author__ = 'ipman'

from django import template


register = template.Library()


@register.inclusion_tag('templatetags/pagination.html')
def public_pagination(page_obj, apps, func, options):
    link = apps+':'+func
    text = ''
    for option in options:
        if text == '':
            text = option
        else:
            text = text+' '+option
    return {'page_obj': page_obj, 'link': link, 'arg_url': text}


@register.inclusion_tag('templatetags/rb_pagination.html')
def rb_pagination(page_obj, apps, func):
    link = apps+':'+func
    return {'page_obj': page_obj, 'link': link, 'arg_url':''}


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()