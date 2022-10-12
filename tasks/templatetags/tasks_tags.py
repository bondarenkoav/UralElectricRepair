from django import template

from repairshop.models import Disassembly, FaultDetection, Mechanics, Tests, Poles, Sections, Inductor, Anchor, \
    Shields, Spindle, Completing, Assembly

__author__ = 'ipman'


register = template.Library()


@register.simple_tag()
def get_repairnum(model_name, record_id):
    repair_num = []
    try:
        if model_name == 'disassembly':
            repair_num = Disassembly.objects.get(id=record_id)
        elif model_name == 'faultdetection':
            repair_num = FaultDetection.objects.get(id=record_id)
        elif model_name == 'mechanics':
            repair_num = Mechanics.objects.get(id=record_id)
        elif model_name == 'tests':
            repair_num = Tests.objects.get(id=record_id)
        elif model_name == 'poles':
            repair_num = Poles.objects.get(id=record_id)
        elif model_name == 'sections':
            repair_num = Sections.objects.get(id=record_id)
        elif model_name == 'inductor':
            repair_num = Inductor.objects.get(id=record_id)
        elif model_name == 'anchor':
            repair_num = Anchor.objects.get(id=record_id)
        elif model_name == 'shields':
            repair_num = Shields.objects.get(id=record_id)
        elif model_name == 'spindle':
            repair_num = Spindle.objects.get(id=record_id)
        elif model_name == 'completing':
            repair_num = Completing.objects.get(id=record_id)
        elif model_name == 'assembly':
            repair_num = Assembly.objects.get(id=record_id)
        return repair_num.equipment
    except:
        pass
