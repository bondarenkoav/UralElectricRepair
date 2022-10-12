import json
import magic
import os

from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_currentuser.middleware import get_current_user

from accounts.models import Profile
from accounts.views import get_cur_branch
from reference_books.forms import ClientForm
from reference_books.models import StatusWork, ModelEquipment, TreeTechProcess
from repairfund import settings
from repairshop.forms import FormAddShipment, ScopeShipmentFormSet, CharactEquipmentFormSet, \
    AssignPerformerForm, ForCheckingDisassemblyForm, ForCheckingFaultDetectionForm, ForCheckingTestsForm, \
    ForCheckingMechanicsForm, ForCheckingPolesForm, ForCheckingCompletingForm, ForCheckingAssemblyForm, \
    ForCheckingSectionsForm, ForCheckingInductorForm, ForCheckingAnchorForm, ForCheckingShieldsForm, \
    ForCheckingSpindleForm, ScopeShipmentUpdateForm, DisassemblyFormSet, FaultDetectionFormSet, MechanicsFormSet, \
    TestsFormSet, StoreFormSet, PolesFormSet, SectionsFormSet, InductorFormSet, AnchorFormSet, ShieldsFormSet, \
    SpindleFormSet, CompletingFormSet, AssemblyFormSet, InvestmentsFormSet
from repairshop.models import ScopeShipment, Shipment, Comments, FaultDetection, Disassembly, Mechanics, Tests, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, Completing, Assembly, Investments, ScopeShipmentEngineFilter, \
    ScopeShipmentTransformersFilter, Storage, Photos
from tasks.views import add_task_appointedperformer, add_task_assignperformer, add_task_verificationpassed, \
    update_task_complete

status_work = StatusWork.objects.all()
model_eq = ModelEquipment.objects.all()


@login_required
@csrf_protect
def add_shipment(request):
    form = FormAddShipment(request.POST or None, request.FILES or None, user=request.user)

    if request.POST:
        if form.is_valid():
            new_shipment = form.save(commit=False)
            new_shipment.branch = get_cur_branch()
            new_shipment.Create_user = request.user
            new_shipment.save()

            return redirect('production:add-scopeshipment', new_shipment.id)

    return render(request, 'repairshop/shipment_item.html', {
        'title': 'Новая поставка',
        'form': form,
        'form_addclient': ClientForm,
    })


@login_required
@csrf_protect
def add_scopeshipment(request, shipment_id):
    shipment_data = Shipment.objects.get(id=shipment_id)

    formset = ScopeShipmentFormSet(queryset=ScopeShipment.objects.filter(shipment=shipment_data))

    if request.POST:
        formset = ScopeShipmentFormSet(data=request.POST)
        for form in formset:
            if form.is_valid():
                if form.cleaned_data['repairnum']:
                    new_scope = form.save(commit=False)
                    new_scope.shipment = shipment_data
                    new_scope.status = StatusWork.objects.get(slug='accepted_repairs')
                    new_scope.Create_user = request.user
                    new_scope.save()
                    messages.success(request, u'Успешно добавлено: %s' % form.cleaned_data['repairnum'])

    return render(request, 'repairshop/scopeshipment_item.html', {
        'title': 'Состав поставки',
        'formset': formset,
        'shipment_data': shipment_data
    })


@login_required
@csrf_protect
def add_charactequipment(request, shipment_id):
    shipment_data = Shipment.objects.get(id=shipment_id)
    formset = CharactEquipmentFormSet(queryset=ModelEquipment.objects.filter(
        id__in=ScopeShipment.objects.filter(
            shipment=shipment_data).values('equipment')))

    if request.POST:
        formset = CharactEquipmentFormSet(data=request.POST)
        for form in formset:
            if form.is_valid():
                form.save()
                messages.success(request, u'Успешно обновлены характеристики: %s.' % form.cleaned_data['name'])

    return render(request, 'repairshop/charact_equipment.html', {
        'title': 'Ввод характеристик оборудования',
        'formset': formset,
        'shipment_data': shipment_data,
    })


@login_required
def getlist_transformers(request):
    qs = ScopeShipment.objects.filter(status__in=status_work.exclude(slug='returned_client'), archive=False,
                                      equipment__in=model_eq.filter(type='transformer'))
    transformers_filter = ScopeShipmentTransformersFilter(request.GET, queryset=qs)
    paginator = Paginator(transformers_filter.qs, 15)
    page = request.GET.get('page')
    try:
        transformers = paginator.page(page)
    except PageNotAnInteger:
        transformers = paginator.page(1)
    except EmptyPage:
        transformers = paginator.page(paginator.num_pages)
        transformers_filter = ScopeShipmentTransformersFilter(request.GET, queryset=qs)

    return render(request, 'repairshop/transform_list.html', {
        'title': 'Трансформаторы',
        'list': transformers,
        'list_filter': transformers_filter,
        'page': page,
    })


@login_required
def getlist_engines_variable(request):
    qs = ScopeShipment.objects.filter(status__in=status_work.exclude(slug='returned_client'), archive=False,
                                      equipment__in=model_eq.filter(type='engine', amperage='variable', p__gte=100))
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)
    paginator = Paginator(engines_filter.qs, 15)
    page = request.GET.get('page')
    try:
        engines = paginator.page(page)
    except PageNotAnInteger:
        engines = paginator.page(1)
    except EmptyPage:
        engines = paginator.page(paginator.num_pages)
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)

    return render(request, 'repairshop/engine_list.html', {
        'title': 'Двигатели переменного тока, больше 100 кВт',
        'type': 'variable',
        'list': engines,
        'list_filter': engines_filter,
        'page': page,
    })


# Постоянка вся
@login_required
def getlist_engines_steady(request):
    qs = ScopeShipment.objects.filter(status__in=status_work.exclude(slug='returned_client'), archive=False,
                                      equipment__in=model_eq.filter(type='engine', amperage='steady'))
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)
    paginator = Paginator(engines_filter.qs, 15)
    page = request.GET.get('page')
    try:
        engines = paginator.page(page)
    except PageNotAnInteger:
        engines = paginator.page(1)
    except EmptyPage:
        engines = paginator.page(paginator.num_pages)
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)

    return render(request, 'repairshop/engine_list.html', {
        'title': 'Двигатели постоянного тока, больше 100 кВт',
        'type': 'steady',
        'list': engines,
        'list_filter': engines_filter,
        'page': page,
    })


# Переменка до 100кВт
@login_required
def getlist_engines_upto100kW(request):
    qs = ScopeShipment.objects.filter(status__in=status_work.exclude(slug='returned_client'), archive=False,
                                      equipment__in=model_eq.filter(type='engine', amperage='variable', p__lt=100))
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)
    paginator = Paginator(engines_filter.qs, 15)
    page = request.GET.get('page')
    try:
        engines = paginator.page(page)
    except PageNotAnInteger:
        engines = paginator.page(1)
    except EmptyPage:
        engines = paginator.page(paginator.num_pages)
    engines_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)

    return render(request, 'repairshop/engine_list.html', {
        'title': 'Двигатели до 100 кВт',
        'list': engines,
        'list_filter': engines_filter,
        'page': page,
    })


@login_required
def getlist_scopeshipment_archive(request):
    qs = ScopeShipment.objects.filter(archive=True)
    ss_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)
    paginator = Paginator(ss_filter.qs, 15)
    page = request.GET.get('page')
    try:
        ss = paginator.page(page)
    except PageNotAnInteger:
        ss = paginator.page(1)
    except EmptyPage:
        ss = paginator.page(paginator.num_pages)
    ss_filter = ScopeShipmentEngineFilter(request.GET, queryset=qs)

    return render(request, 'repairshop/scopeshipment_archive_list.html', {
        'title': 'Архив',
        'type': 'variable',
        'list': ss,
        'list_filter': ss_filter,
        'page': page,
    })


def save_client(request):
    client_form = ClientForm(request.POST or None)
    response_data = {}
    if request.method == 'POST':
        response_data['name_client'] = request.POST['name']
        if client_form.is_valid():
            client_form.save()
            response_data['msg'] = 'добавлен успешно'
        else:
            response_data['msg'] = 'ошибка данных'
        return HttpResponse(
            json.dumps(response_data), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
@csrf_protect
def scopeshipment_update(request, pk):
    sc_data = ScopeShipment.objects.get(id=pk)
    comments = Comments.objects.filter(equipment=sc_data)

    form = ScopeShipmentUpdateForm(request.POST or None, instance=pk and ScopeShipment.objects.get(id=pk))

    if sc_data.equipment.type == 'engine':
        if sc_data.equipment.p > 100:
            if sc_data.equipment.amperage == 'variable':
                url_listengines = reverse('engines-variable')
            else:
                url_listengines = reverse('engines-steady')
        else:
            url_listengines = reverse('engines-upto100kW')
    else:
        url_listengines = reverse('transformers')

    if request.POST:
        if form.is_valid():
            new_data = form.save(commit=False)
            new_data.save()
            messages.success(request, u'Успешно обновлены данные разборки')

    return render(request, 'repairshop/scopeshipment_form.html', {
        'title': 'Ремонтный %s от %s' % (sc_data.repairnum, sc_data.shipment.dateshipment),
        'form': form,
        'sc_data': sc_data,
        'comments': comments,
        'url_listengines': url_listengines
    })


@login_required
@csrf_protect
def scopeshipment_archive(request, pk):
    sc_data = ScopeShipment.objects.get(id=pk)
    comments = Comments.objects.filter(equipment=sc_data)

    return render(request, 'repairshop/scopeshipment_archive.html', {
        'title': 'Ремонтный %s от %s' % (sc_data.repairnum, sc_data.shipment.dateshipment),
        'sc_data': sc_data,
        'comments': comments,
    })


# -----------------------------------------------------------------------------------------------------
# - 10 ----------------------- Редактирование вкладок сводной формы -----------------------------------
# -----------------------------------------------------------------------------------------------------
def update_disassembly_tab(request, pk):
    title = 'Разборка'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = DisassemblyFormSet(queryset=Disassembly.objects.filter(equipment=sc_data))

    if request.POST:
        formset = DisassemblyFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Disassembly.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='disassembly',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(), receiving=new_data.receiving, 
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data['executor']:
                                    add_task_appointedperformer(app_name='production', model_name='disassembly',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-disassembly',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)

                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_disassembly.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_faultdetection_tab(request, pk):
    title = 'Дефектация'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = FaultDetectionFormSet(queryset=FaultDetection.objects.filter(equipment=sc_data))

    if request.POST:
        formset = FaultDetectionFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        FaultDetection.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='faultdetection',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name,
                                                         curr_user=get_current_user(), receiving=new_data.receiving,
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='faultdetection',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-faultdetection',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_faultdetection.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_mechanics_tab(request, pk):
    title = 'Механика'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = MechanicsFormSet(queryset=Mechanics.objects.filter(equipment=sc_data))

    if request.POST:
        formset = MechanicsFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Mechanics.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='mechanics',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name,
                                                         curr_user=get_current_user(), receiving=new_data.receiving,
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='mechanics',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-mechanics',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)

                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                    
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_mechanics.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_tests_tab(request, pk):
    title = 'Испытание'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = TestsFormSet(queryset=Tests.objects.filter(equipment=sc_data))

    if request.POST:
        formset = TestsFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Tests.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='tests',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.indications,
                                                         curr_user=get_current_user(),
                                                         receiving=new_data.receiving, date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='tests',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-tests',
                                                                title=title, name=new_data.indications,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.indications)
                    
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_tests.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_storage_tab(request, pk):
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = StoreFormSet(queryset=Storage.objects.filter(equipment=sc_data))

    if request.POST:
        formset = StoreFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Storage.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()

                        messages.success(request, u'%s - успешно сохранено' % new_data.detail.name)
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_store.html', {
        'title': 'Склад',
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_poles_tab(request, pk):
    title = 'Полюса'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = PolesFormSet(queryset=Poles.objects.filter(equipment=sc_data))

    if request.POST:
        formset = PolesFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Poles.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='poles',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name,
                                                         curr_user=get_current_user(), receiving=new_data.receiving,
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='poles',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-poles',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                    
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-poles-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_sections_tab(request, pk):
    title = 'Секции'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = SectionsFormSet(queryset=Sections.objects.filter(equipment=sc_data))

    if request.POST:
        formset = SectionsFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Sections.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='sections',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name,
                                                         curr_user=get_current_user(), receiving=new_data.receiving,
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='sections',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-sections',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)

                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-sections-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_inductor_tab(request, pk):
    title = 'Индуктор'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = InductorFormSet(queryset=Inductor.objects.filter(equipment=sc_data))

    if request.POST:
        formset = InductorFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Inductor.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='inductor',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name,
                                                         curr_user=get_current_user(), receiving=new_data.receiving,
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='inductor',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-inductor',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                    
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-inductor-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_anchor_tab(request, pk):
    title = 'Якорь'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = AnchorFormSet(queryset=Anchor.objects.filter(equipment=sc_data))

    if request.POST:
        formset = AnchorFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Anchor.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='anchor',
                                                         fun_name='assignperformer', record_pk=new_data.id, 
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(),
                                                         receiving=new_data.receiving, date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='anchor',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-anchor',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)

                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-anchor-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_shields_tab(request, pk):
    title = 'Щиты'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = ShieldsFormSet(queryset=Shields.objects.filter(equipment=sc_data))

    if request.POST:
        formset = ShieldsFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Shields.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='shields',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(), receiving=new_data.receiving, 
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='shields',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-shields',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)

                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-shields-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_spindle_tab(request, pk):
    title = 'Вал'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = SpindleFormSet(queryset=Spindle.objects.filter(equipment=sc_data))

    if request.POST:
        formset = SpindleFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Spindle.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='spindle',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(), receiving=new_data.receiving, 
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='spindle',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id,
                                                                _url='mobile:appointed-performer-spindle',
                                                                title=title, name=new_data.name,
                                                                curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)

                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_components.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'url_save': reverse('production:update-spindle-tab', kwargs={'pk': pk}),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_completing_tab(request, pk):
    title = 'Комплектование'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = CompletingFormSet(queryset=Completing.objects.filter(equipment=sc_data))

    if request.POST:
        formset = CompletingFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Completing.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='completing',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(), receiving=new_data.receiving, 
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='completing',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id, _url='mobile:appointed-performer-completing',
                                                                title=title, name=new_data.name, curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)

                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_completing.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_assembly_tab(request, pk):
    title = 'Сборка'
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = AssemblyFormSet(queryset=Assembly.objects.filter(equipment=sc_data))

    if request.POST:
        formset = AssemblyFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    record = form.cleaned_data["id"]
                    if form.cleaned_data["DELETE"]:
                        Assembly.objects.filter(id=record.pk).delete()
                    else:
                        new_data = form.save(commit=False)
                        new_data.equipment = sc_data
                        new_data.save()
                        form.save_m2m()

                        if new_data.date_due is not None and new_data.complete is False:
                            if form.cleaned_data.get('executor') is None:
                                add_task_assignperformer(app_name='production', model_name='assembly',
                                                         fun_name='assignperformer', record_pk=new_data.id,
                                                         sc_pk=sc_data.id, title=title, name=new_data.name, 
                                                         curr_user=get_current_user(), receiving=new_data.receiving, 
                                                         date_due=new_data.date_due)
                            else:
                                for executor in form.cleaned_data.get('executor'):
                                    add_task_appointedperformer(app_name='production', model_name='assembly',
                                                                fun_name='appointedperformer', record_pk=new_data.id,
                                                                sc_pk=sc_data.id, _url='mobile:appointed-performer-assembly',
                                                                title=title, name=new_data.name, curr_user=get_current_user(),
                                                                executor=executor, date_due=new_data.date_due)
                    
                        messages.success(request, u'%s - успешно сохранено' % new_data.name)
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_assembly.html', {
        'title': title,
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


def update_investments_tab(request, pk):
    sc_data = ScopeShipment.objects.get(id=pk)
    formset = InvestmentsFormSet(queryset=Investments.objects.filter(equipment=sc_data))

    if request.POST:
        formset = InvestmentsFormSet(request.POST, request.FILES)
        for form in formset:
            if form.is_valid():
                try:
                    # name = form.cleaned_data['key']
                    new_data = form.save(commit=False)
                    new_data.equipment = sc_data
                    new_data.save()
                    messages.success(request, u'%s - успешно сохранено' % new_data.key)
                except:
                    pass

    return render(request, 'repairshop/templatetags/formset_investments.html', {
        'title': 'Вложения',
        'title_small': 'Ремонтный №%s от %s.' % (sc_data.repairnum, sc_data.shipment.dateshipment.strftime('%d.%m.%Y')),
        'formset': formset,
        'sc_data': sc_data,
    })


# -----------------------------------------------------------------------------------------------------
# ------------------------------- Заполнение форрмсетов во вкладках -----------------------------------
# -----------------------------------------------------------------------------------------------------
@csrf_exempt
def fill_tabs(request, pk):
    if request.POST:
        sc_data = ScopeShipment.objects.get(pk=pk)
        category = TreeTechProcess.objects.get(id=request.POST['template_id'])

        if category:
            root = category.get_root()
            children = category.get_children()

            for item in children:
                if root.slug == 'faultdetection':
                    FaultDetection.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'mechanics':
                    Mechanics.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'tests':
                    Tests.objects.create(equipment=sc_data, indications=item.name)
                elif root.slug == 'poles':
                    Poles.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'sections':
                    Sections.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'inductor':
                    Inductor.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'anchor':
                    Anchor.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'shields':
                    Shields.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'spindle':
                    Spindle.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'completing':
                    Completing.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                elif root.slug == 'assembly':
                    Assembly.objects.create(equipment=sc_data, name=item.name, group_receiving=item.responsible_group)
                else:
                    return HttpResponse('error')
        return HttpResponse('success')

# -----------------------------------------------------------------------------------------------------
# ---------------------------------- Добавление комментариев ------------------------------------------
# -----------------------------------------------------------------------------------------------------
@login_required
@csrf_exempt
def add_comment_scopeshipment(request, pk):
    if request.POST:
        post_text = request.POST['the_post']

        if post_text != '':
            response_data = {}
            post = Comments(equipment=ScopeShipment.objects.get(pk=pk), text=post_text)
            post.save()

            response_data['result'] = 'Добавлен комментарий!'
            response_data['postpk'] = post.pk
            response_data['text'] = post.text
            response_data['created'] = post.datetime_add.strftime('%d.%m.%Y %H:%M')
            response_data['author'] = post.create_user.username

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"ничего не прилетело"}),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"ничего не прилетело"}),
            content_type="application/json"
        )


# -----------------------------------------------------------------------------------------------------
# ---------------------------------- Назначение исполнителя -------------------------------------------
# -----------------------------------------------------------------------------------------------------
@login_required
@csrf_protect
def assign_performer(request, type, pk):
    form = AssignPerformerForm(request.POST or None)
    title = ''

    if request.POST:
        if form.is_valid():
            executor = form.cleaned_data.get('executor')
            if type == 'disassembly':
                data = Disassembly.objects.get(id=pk)
                title = 'Разборка'
                name = data.name
                Disassembly.objects.filter(id=pk).update(executor=executor)
            elif type == 'faultdetection':
                data = FaultDetection.objects.get(id=pk)
                title = 'Дефектация'
                name = data.name
                FaultDetection.objects.filter(id=pk).update(executor=executor)
            elif type == 'mechanics':
                data = Mechanics.objects.get(id=pk)
                title = 'Механика'
                name = data.name
                Mechanics.objects.filter(id=pk).update(executor=executor)
            elif type == 'tests':
                data = Tests.objects.get(id=pk)
                title = 'Испытание'
                name = data.indications
                Tests.objects.filter(id=pk).update(executor=executor)
            elif type == 'poles':
                data = Poles.objects.get(id=pk)
                title = 'Полюса'
                name = data.name
                Poles.objects.filter(id=pk).update(executor=executor)
            elif type == 'sections':
                data = Sections.objects.get(id=pk)
                title = 'Секции'
                name = data.name
                Sections.objects.filter(id=pk).update(executor=executor)
            elif type == 'inductor':
                data = Inductor.objects.get(id=pk)
                title = 'Индуктор/Статор'
                name = data.name
                Inductor.objects.filter(id=pk).update(executor=executor)
            elif type == 'anchor':
                data = Anchor.objects.get(id=pk)
                title = 'Якорь/Ротор'
                name = data.name
                Anchor.objects.filter(id=pk).update(executor=executor)
            elif type == 'shields':
                data = Shields.objects.get(id=pk)
                title = 'Щиты'
                name = data.name
                Shields.objects.filter(id=pk).update(executor=executor)
            elif type == 'spindle':
                data = Spindle.objects.get(id=pk)
                title = 'Вал'
                name = data.name
                Spindle.objects.filter(id=pk).update(executor=executor)
            elif type == 'completing':
                data = Completing.objects.get(id=pk)
                title = 'Комплектование'
                name = data.name
                Completing.objects.filter(id=pk).update(executor=executor)
            elif type == 'assembly':
                data = Assembly.objects.get(id=pk)
                title = 'Сборка'
                name = data.name
                Assembly.objects.filter(id=pk).update(executor=executor)
            else:
                data = name = None

            if data:
                if executor:
                    update_task_complete(app_name='production', model_name=type, fun_name='assignperformer', record_pk=pk)
                add_task_appointedperformer(app_name='production', model_name=type, fun_name='appointedperformer',
                                            record_pk=pk, _url='mobile:appointed-performer-%s' % type,
                                            title=title, name=name, curr_user=get_current_user(),
                                            executor=executor, date_due=data.date_due)

            return redirect('production:scopeshipment-update', data.equipment.pk)

    return render(request, 'repairshop/assign_performer.html', {
        'title': 'Определение исполнителя',
        'form': form,
        'type': type,
        'type_pk': pk
    })


# -----------------------------------------------------------------------------------------------------
# -------------------------------------- Проверка ОТК -------------------------------------------------
# -----------------------------------------------------------------------------------------------------
@login_required
@csrf_protect
def forchecking_disassembly(request, pk):
    sc_data = Disassembly.objects.get(id=pk).equipment
    form = ForCheckingDisassemblyForm(request.POST or None, request.FILES or None,
                                      instance=pk and Disassembly.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Disassembly.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            # new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            if form.cleaned_data['photo']:
                p = Photos.objects.create(equipment=old_data.equipment, photo=form.cleaned_data['photo'])
                new_form.images.add(p)
            new_form.save()

            update_task_complete(app_name='production', model_name='disassembly', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='disassembly',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Разборка', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль разборки',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-disassembly', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_faultdetection(request, pk):
    sc_data = FaultDetection.objects.get(id=pk).equipment
    form = ForCheckingFaultDetectionForm(request.POST or None, request.FILES or None,
                                         instance=pk and FaultDetection.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = FaultDetection.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            if form.cleaned_data['photo']:
                p = Photos.objects.create(equipment=old_data.equipment, photo=form.cleaned_data['photo'])
                new_form.images.add(p)
            new_form.save()

            update_task_complete(app_name='production', model_name='faultdetection', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='faultdetection',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Дефектация', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: дефектация',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-faultdetection', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_mechanics(request, pk):
    sc_data = Mechanics.objects.get(id=pk).equipment
    form = ForCheckingMechanicsForm(request.POST or None, request.FILES or None,
                                    instance=pk and Mechanics.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Mechanics.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            if form.cleaned_data['photo']:
                p = Photos.objects.create(equipment=old_data.equipment, photo=form.cleaned_data['photo'])
                new_form.images.add(p)
            new_form.save()

            update_task_complete(app_name='production', model_name='mechanics', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='mechanics',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Механика', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: механика',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-mechanics', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_tests(request, pk):
    sc_data = Tests.objects.get(id=pk).equipment
    form = ForCheckingTestsForm(request.POST or None, request.FILES or None, instance=pk and Tests.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Tests.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.executor = old_data.executor
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            if form.cleaned_data['photo']:
                p = Photos.objects.create(equipment=old_data.equipment, photo=form.cleaned_data['photo'])
                new_form.images.add(p)
            new_form.save()

            update_task_complete(app_name='production', model_name='tests', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='tests',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Испытание', name=old_data.indications,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: испытание',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-tests', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_poles(request, pk):
    sc_data = Poles.objects.get(id=pk).equipment
    form = ForCheckingPolesForm(request.POST or None, instance=pk and Poles.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Poles.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='poles', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='poles',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Полюса', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: полюса',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-poles', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_sections(request, pk):
    sc_data = Sections.objects.get(id=pk).equipment
    form = ForCheckingSectionsForm(request.POST or None, instance=pk and Sections.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Sections.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='sections', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='sections',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Секции', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: секции',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-sections', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_inductor(request, pk):
    sc_data = Inductor.objects.get(id=pk).equipment
    form = ForCheckingInductorForm(request.POST or None, instance=pk and Inductor.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Inductor.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='inductor', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='inductor',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Индуктор', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: Индуктор/Статор',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-inductor', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_anchor(request, pk):
    sc_data = Anchor.objects.get(id=pk).equipment
    form = ForCheckingAnchorForm(request.POST or None, instance=pk and Anchor.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Anchor.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='anchor', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='anchor',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Якорь', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: Якорь/Ротор',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-anchor', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_shields(request, pk):
    sc_data = Shields.objects.get(id=pk).equipment
    form = ForCheckingShieldsForm(request.POST or None, instance=pk and Shields.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Shields.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='shields', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='shields',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Щиты', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: Щиты',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-shields', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_spindle(request, pk):
    sc_data = Spindle.objects.get(id=pk).equipment
    form = ForCheckingSpindleForm(request.POST or None, instance=pk and Spindle.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Spindle.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='spindle', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='spindle',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Вал', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль: вал',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-spindle', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_completing(request, pk):
    sc_data = Completing.objects.get(id=pk).equipment
    form = ForCheckingCompletingForm(request.POST or None, instance=pk and Completing.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Completing.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='completing', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='completing',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Комплектование', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль комплектования',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-completing', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def forchecking_assembly(request, pk):
    sc_data = Assembly.objects.get(id=pk).equipment
    form = ForCheckingAssemblyForm(request.POST or None, instance=pk and Assembly.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Assembly.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.name = old_data.name
            new_form.executor = old_data.executor
            new_form.date_complete = old_data.date_complete
            new_form.receiving = Profile.objects.get(user=request.user)
            new_form.date_receiving = datetime.today()
            new_form.save()

            update_task_complete(app_name='production', model_name='assembly', fun_name='forchecking', record_pk=old_data.id)
            add_task_verificationpassed(app_name='production', model_name='assembly',
                                        fun_name='verificationpassed', sc_pk=old_data.equipment.pk,
                                        record_pk=old_data.id, title='Сборка', name=old_data.name,
                                        curr_user=get_current_user())

            return redirect('production:scopeshipment-update', old_data.equipment.pk)

    return render(request, 'repairshop/for_checking.html', {
        'title': 'Контроль сборки',
        'sc_data': sc_data,
        'form': form,
        'url_': reverse('production:forchecking-assembly', kwargs={'pk': pk}),
    })


# -----------------------------------------------------------------------------------------------------
# -------------------------------------- Отдача файла -------------------------------------------------
# -----------------------------------------------------------------------------------------------------
def get_files(request, type, pk):
    if type == 'faultdetection':
        path = FaultDetection.objects.get(id=pk).photo.path
    elif type == 'mechanics':
        path = Mechanics.objects.get(id=pk).photo.path
    elif type == 'tests':
        path = Tests.objects.get(id=pk).photo.path
    elif type == 'investments':
        path = Investments.objects.get(id=pk).file.path
    else:
        path = reverse('no_image.jpeg')

    mf = magic.from_file(path, mime=True)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mf)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# -----------------------------------------------------------------------------------------------------
# -------------------------------------- Список поставок ----------------------------------------------
# -----------------------------------------------------------------------------------------------------
@login_required
def getlist_shipments(request):
    paginator = Paginator(Shipment.objects.all().order_by('-datetime_add'), 20)

    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'repairshop/shipment_list.html', {
        'list': list,
        'page': page,
    })


@login_required
def get_shipment(request, pk):
    shipment_data = Shipment.objects.get(id=pk)
    scshipment_data = ScopeShipment.objects.filter(shipment=shipment_data)

    return render(request, 'repairshop/delivery_description.html', {
        'shipment': shipment_data,
        'scshipment': scshipment_data
    })

