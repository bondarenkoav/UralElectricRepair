from django import template
from django.core.exceptions import ObjectDoesNotExist

from repairshop.models import Disassembly, FaultDetection, Mechanics, Tests, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, Completing, Assembly

__author__ = 'ipman'


register = template.Library()


def get_status_complete(model_name, record_id):
    qs = True
    try:
        if model_name == 'disassembly':
            qs = Disassembly.objects.get(id=record_id).complete
        elif model_name == 'faultdetection':
            qs = FaultDetection.objects.get(id=record_id).complete
        elif model_name == 'mechanics':
            qs = Mechanics.objects.get(id=record_id).complete
        elif model_name == 'tests':
            qs = Tests.objects.get(id=record_id).complete
        elif model_name == 'poles':
            qs = Poles.objects.get(id=record_id).complete
        elif model_name == 'sections':
            qs = Sections.objects.get(id=record_id).complete
        elif model_name == 'inductor':
            qs = Inductor.objects.get(id=record_id).complete
        elif model_name == 'anchor':
            qs = Anchor.objects.get(id=record_id).complete
        elif model_name == 'shields':
            qs = Shields.objects.get(id=record_id).complete
        elif model_name == 'spindle':
            qs = Spindle.objects.get(id=record_id).complete
        elif model_name == 'completing':
            qs = Completing.objects.get(id=record_id).complete
        elif model_name == 'assembly':
            qs = Assembly.objects.get(id=record_id).complete
        return qs
    except ObjectDoesNotExist:
        return True


@register.inclusion_tag('mobile/templatetags/mobile_tasks_list_tag.html')
def get_mobiletask_list_tag(item):
    complete = get_status_complete(item.model_name, item.record_id)
    if complete is False:
        return {'item': item}


@register.inclusion_tag('mobile/templatetags/mobile_archive_list_tag.html')
def get_archive_list_tag(item):
    complete = get_status_complete(item.model_name, item.record_id)
    return {'item': item, 'complete': complete}
