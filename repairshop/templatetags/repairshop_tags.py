from django import template

from reference_books.models import ResultsDetailTechProcess, TreeTechProcess
from repairshop.models import Disassembly, FaultDetection, Mechanics, Tests, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, \
    Completing, Assembly, Investments, Storage, ScopeShipment

__author__ = 'ipman'


register = template.Library()


@register.inclusion_tag('repairshop/templatetags/table_disassembly.html')
def get_table_disassembly(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Disassembly.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_faultdetection.html')
def get_table_faultdetection(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': FaultDetection.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_mechanics.html')
def get_table_mechanics(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Mechanics.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_tests.html')
def get_table_tests(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Tests.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_storage.html')
def get_table_storage(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Storage.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_poles(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Poles.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_sections(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Sections.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_inductor(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Inductor.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_anchor(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Anchor.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_shields(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Shields.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_components.html')
def get_table_spindle(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Spindle.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_completing.html')
def get_table_completing(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Completing.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_assembly.html')
def get_table_assembly(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Assembly.objects.filter(equipment=scoupeshipment_id)}


@register.inclusion_tag('repairshop/templatetags/table_investments.html')
def get_table_investments(scoupeshipment_id):
    return {'sc_id': scoupeshipment_id, 'table_data': Investments.objects.filter(equipment=scoupeshipment_id)}


@register.simple_tag()
def get_techprocess_fielddata(techprocess, field, scoupeshipment):
    if techprocess == 'disassembly':
        qt = Disassembly.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'faultdetection':
        qt = FaultDetection.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'mechanics':
        qt = Mechanics.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'tests':
        qt = Tests.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'poles':
        qt =  Poles.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'sections':
        qt = Sections.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'inductor':
        qt = Inductor.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'anchor':
        qt = Anchor.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'shields':
        qt = Shields.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'spindle':
        qt = Spindle.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'completing':
        qt = Completing.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    elif techprocess == 'assembly':
        qt = Assembly.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
    else:
        qt = Disassembly.objects.none()

    if qt:
        if field == 'name':
            return qt.order_by('id').values_list('name', flat=True).last()
        elif field == 'date_complete':
            return qt.order_by('id').values_list('date_complete', flat=True).last()
        else:
            return ''
    else:
        return ''


@register.simple_tag()
def get_techprocess_fieldcolor(techprocess, scoupeshipment):
    qt = Disassembly.objects.none()

    if techprocess in ['disassembly', 'tests']:
        if techprocess == 'disassembly':
            qt =  Disassembly.objects.filter(equipment=scoupeshipment, executor__isnull=False)
        elif techprocess == 'tests':
            qt = Tests.objects.filter(equipment=scoupeshipment, executor__isnull=False)
        if qt:
            qt = qt.values_list('complete', flat=True).order_by('id').last()
            if qt is True:
                return 'table-success'
    elif techprocess in ['faultdetection', 'poles', 'sections', 'inductor', 'anchor', 'shields', 'spindle', 'completing', 'assembly']:
        if techprocess == 'faultdetection':
            qt = FaultDetection.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'mechanics':
            qt = Mechanics.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'poles':
            qt = Poles.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'sections':
            qt = Sections.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'inductor':
            qt = Inductor.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'anchor':
            qt = Anchor.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'shields':
            qt = Shields.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'spindle':
            qt = Spindle.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'completing':
            qt = Completing.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        elif techprocess == 'assembly':
            qt = Assembly.objects.filter(equipment=scoupeshipment, date_due__isnull=False)  # executor__isnull=False
        if qt:
            complete = qt.values_list('complete', flat=True).order_by('id').last()
            result = qt.values_list('result', flat=True).order_by('id').last()
            if result:
                result_slug = ResultsDetailTechProcess.objects.get(id=result).slug
            else:
                result_slug = ''
            if complete is True and result_slug is None:
                return 'table - warning'
            elif result_slug == 'accepted':
                return 'table - success'
            elif result_slug == 'reject':
                return 'table - danger'
            elif result_slug == 'modification':
                return 'table - warning'
        else:
            return 'table-active'
    else:
        return 'table-active'


@register.simple_tag()
def get_techprocess_data(techprocess, pk):
    if pk:
        if techprocess == 'disassembly':
            return Disassembly.objects.get(id=int(pk))
        elif techprocess == 'faultdetection':
            return FaultDetection.objects.get(id=int(pk))
        elif techprocess == 'mechanics':
            return Mechanics.objects.get(id=int(pk))
        elif techprocess == 'tests':
            return Tests.objects.get(id=int(pk))
        elif techprocess == 'poles':
            return Poles.objects.get(id=int(pk))
        elif techprocess == 'sections':
            return Sections.objects.get(id=int(pk))
        elif techprocess == 'inductor':
            return Inductor.objects.get(id=int(pk))
        elif techprocess == 'anchor':
            return Anchor.objects.get(id=int(pk))
        elif techprocess == 'shields':
            return Shields.objects.get(id=int(pk))
        elif techprocess == 'spindle':
            return Spindle.objects.get(id=int(pk))
        elif techprocess == 'completing':
            return Completing.objects.get(id=int(pk))
        elif techprocess == 'assembly':
            return Assembly.objects.get(id=int(pk))
        elif techprocess == 'investments':
            return Investments.objects.get(id=int(pk))
        else:
            return []
    else:
        return []


# Определение типа файла
@register.inclusion_tag('repairshop/templatetags/icon_file_ext.html')
def get_icon_file_ext(path):
    file_ext = '.' + path.split('.')[-1]
    return {'ext': file_ext}


# Количество оборудования в поставке
@register.simple_tag()
def get_count_scoupshipment(shipment_id):
    return ScopeShipment.objects.filter(shipment=int(shipment_id)).count()


@register.inclusion_tag('tasks/templatetags/planned_techpro_accitem.html')
def getlist_planning_techprocess(root_node_name):
    eq_under_repair = ScopeShipment.objects.filter(archive=False)
    if root_node_name == 'disassembly':
        processes = Disassembly.objects.filter(equipment__in=eq_under_repair, accepted=False)
    elif root_node_name == 'faultdetection':
        processes = FaultDetection.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'mechanics':
        processes = Mechanics.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'tests':
        processes = Tests.objects.filter(equipment__in=eq_under_repair, complete=False)
    elif root_node_name == 'poles':
        processes = Poles.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'sections':
        processes = Sections.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'inductor':
        processes = Inductor.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'anchor':
        processes = Anchor.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'shields':
        processes = Shields.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'spindle':
        processes = Spindle.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'completing':
        processes = Completing.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    elif root_node_name == 'assembly':
        processes = Assembly.objects.filter(equipment__in=eq_under_repair, result__isnull=True)
    else:
        processes = None

    return {'root_node': root_node_name, 'processes': processes}


@register.inclusion_tag('tasks/templatetags/planned_techpro_listEq.html')
def getlist_planning_equipment(root_node_name, process_name):
    if root_node_name == 'disassembly':
        list_eq = Disassembly.objects.filter(name=process_name, accepted=False)
    elif root_node_name == 'faultdetection':
        list_eq = FaultDetection.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'mechanics':
        list_eq = Mechanics.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'tests':
        list_eq = Tests.objects.filter(indications=process_name, complete=False)
    elif root_node_name == 'poles':
        list_eq = Poles.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'sections':
        list_eq = Sections.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'inductor':
        list_eq = Inductor.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'anchor':
        list_eq = Anchor.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'shields':
        list_eq = Shields.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'spindle':
        list_eq = Spindle.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'completing':
        list_eq = Completing.objects.filter(name=process_name, result__isnull=True)
    elif root_node_name == 'assembly':
        list_eq = Assembly.objects.filter(name=process_name, result__isnull=True)
    else:
        list_eq = None

    return {'list_equipment': list_eq}