from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django_currentuser.middleware import get_current_user

from accounts.models import Profile
from mobile.forms import ToPerformDisassemblyForm, ToPerformFaultDetectionForm, ToPerformMechanicsForm, \
    ToPerformTestsForm, ToPerformPolesForm, ToPerformCompletingForm, ToPerformAssemblyForm, ToPerformSectionsForm, \
    ToPerformInductorForm, ToPerformAnchorForm, ToPerformShieldsForm, ToPerformSpindleForm, ArchiveForm
from repairshop.models import Disassembly, FaultDetection, Mechanics, Tests, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, Completing, Assembly, Photos
from tasks.models import Tasks
from tasks.views import add_task_forchecking, update_task_complete


@login_required
def getlist_tasks_mobile(request):
    archive = []
    tasks = Tasks.objects.filter(executor=Profile.objects.get(user=get_current_user()), complete=False)
    form = ArchiveForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            start_period = form.cleaned_data['start_period']
            end_period = form.cleaned_data['end_period']

            archive = Tasks.objects.filter(executor=Profile.objects.get(user=request.user),
                                           datetime_update__range=(start_period, end_period))

    return render(request, 'mobile/mobile_task_list.html', {
        'title': 'Задачи',
        'tasks': tasks,
        'archive': archive,
        'form_archive': form,
        'curr_user': get_current_user()
    })


@login_required
@csrf_protect
def getitem_task_mobile(request, pk):
    Tasks.objects.filter(id=pk).update(read=True)

    return render(request, 'tasks/tasks_item.html', {
        'title': 'Задача',
        'task_data': Tasks.objects.get(id=pk),
    })


@login_required
@csrf_protect
def appointedperformer_disassembly(request, pk):
    title = 'Разборка'
    sc_data = Disassembly.objects.get(id=pk).equipment
    form = ToPerformDisassemblyForm(request.POST or None, request.FILES or None,
                                    instance=pk and Disassembly.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Disassembly.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            if form.cleaned_data['photo']:
                p = Photos.objects.create(equipment=old_data.equipment, photo=form.cleaned_data['photo'])
                new_form.images.set([p])
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='disassembly', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='disassembly', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-disassembly',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Disassembly.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-disassembly', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_faultdetection(request, pk):
    title = 'Дефектация'
    sc_data = FaultDetection.objects.get(id=pk).equipment
    form = ToPerformFaultDetectionForm(request.POST or None, request.FILES or None,
                                       instance=pk and FaultDetection.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = FaultDetection.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='faultdetection', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='faultdetection', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-faultdetection',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': FaultDetection.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-faultdetection', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_mechanics(request, pk):
    title = 'Механика'
    sc_data = Mechanics.objects.get(id=pk).equipment
    form = ToPerformMechanicsForm(request.POST or None, request.FILES or None,
                                  instance=pk and Mechanics.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Mechanics.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='mechanics', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='mechanics', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-mechanics',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Mechanics.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-mechanics', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_tests(request, pk):
    title = 'Испытания'
    sc_data = Tests.objects.get(id=pk).equipment
    form = ToPerformTestsForm(request.POST or None, request.FILES or None,
                              instance=pk and Tests.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Tests.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='tests', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='tests', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-tests',
                                 title=title, name=old_data.indications, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Tests.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-tests', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_poles(request, pk):
    title = 'Полюса'
    sc_data = Poles.objects.get(id=pk).equipment
    form = ToPerformPolesForm(request.POST or None, instance=pk and Poles.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Poles.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='poles', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='poles', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-poles',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Poles.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-poles', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_sections(request, pk):
    title = 'Секции'
    sc_data = Sections.objects.get(id=pk).equipment
    form = ToPerformSectionsForm(request.POST or None, instance=pk and Sections.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Sections.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='sections', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='sections', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-sections',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': 'Секции',
        'sc_data': sc_data,
        'ap_data': Sections.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-sections', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_inductor(request, pk):
    title = 'Индуктор/Статор'
    sc_data = Inductor.objects.get(id=pk).equipment
    form = ToPerformInductorForm(request.POST or None, instance=pk and Inductor.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Inductor.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='inductor', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='inductor', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-inductor',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Inductor.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-inductor', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_anchor(request, pk):
    title = 'Якорь/Ротор'
    sc_data = Anchor.objects.get(id=pk).equipment
    form = ToPerformAnchorForm(request.POST or None, instance=pk and Anchor.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Anchor.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='anchor', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='anchor', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-anchor',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Anchor.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-anchor', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_shields(request, pk):
    title = 'Щиты'
    sc_data = Shields.objects.get(id=pk).equipment
    form = ToPerformShieldsForm(request.POST or None, instance=pk and Shields.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Shields.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='shields', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='shields', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-shields',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Shields.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-shields', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_spindle(request, pk):
    title = 'Вал'
    sc_data = Spindle.objects.get(id=pk).equipment
    form = ToPerformSpindleForm(request.POST or None, instance=pk and Spindle.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Spindle.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='spindle', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='spindle', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-spindle',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Spindle.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-spindle', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_completing(request, pk):
    title = 'Комплектование'
    sc_data = Completing.objects.get(id=pk).equipment
    form = ToPerformCompletingForm(request.POST or None, instance=pk and Completing.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Completing.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='completing', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='completing', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-completing',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Completing.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-completing', kwargs={'pk': pk}),
    })


@login_required
@csrf_protect
def appointedperformer_assembly(request, pk):
    title = 'Сборка'
    sc_data = Assembly.objects.get(id=pk).equipment
    form = ToPerformAssemblyForm(request.POST or None, instance=pk and Assembly.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            old_data = Assembly.objects.get(id=pk)
            new_form = form.save(commit=False)
            new_form.date_complete = datetime.today()
            new_form.save()

            if form.cleaned_data['complete'] is True:
                update_task_complete(app_name='production', model_name='assembly', fun_name='appointedperformer',
                                     record_pk=old_data.id)
            add_task_forchecking(app_name='production', model_name='assembly', fun_name='forchecking',
                                 record_pk=old_data.id, sc_pk=sc_data.id, _url='production:forchecking-assembly',
                                 title=title, name=old_data.name, curr_user=get_current_user(),
                                 receiving=old_data.receiving)

            return redirect('mobile:getlist-executor-tasks')

    return render(request, 'mobile/toperform.html', {
        'title': title,
        'sc_data': sc_data,
        'ap_data': Assembly.objects.get(id=pk),
        'form': form,
        'url_': reverse('mobile:appointed-performer-assembly', kwargs={'pk': pk}),
    })
