# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from reference_books.forms import ClientForm, PostForm, EquipmentForm
from reference_books.models import Client, Posts, ModelEquipment, TreeTechProcess

url_area = 'reference_books'
logger = logging.getLogger(__name__)


def client_names(name):
    name = name.replace('"', '')
    name = name.strip(' ')

    OKOPF = ['ООО', 'ЗАО', 'АО', 'ПАО', 'ИП']
    name_massiv = name.split(' ')

    for item in OKOPF:
        if name_massiv[0] == item:
            name = name.replace(item,'') + ' ' + item.__str__()

    name = name.strip(' ')
    return name


@login_required
def getlist_clients(request):
    paginator = Paginator(Client.objects.all(), 20)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'reference_books/clients_list.html', {
        'title': 'Контрагенты',
        'list': list,
        'page': page,
    })


@login_required
@csrf_protect
def update_client(request, pk):
    form = ClientForm(request.POST or None, instance=pk and Client.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('rbooks:getlist_clients')
    else:
        return render(request, 'reference_books/clients_item.html', {
            'title': 'Контрагент',
            'client_id': pk,
            'form': form,
        })
    

@login_required
@csrf_protect
def update_clientforshipment(request, client_id, shipment_id):
    form = ClientForm(request.POST or None, instance=client_id and Client.objects.get(id=client_id))
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('production:add-scopeshipment', shipment_id)

    return render(request, 'reference_books/clients_item.html', {
        'title': 'Дополните данные контрагента',
        'client_data': Client.objects.get(id=client_id),
        'shipment_id': shipment_id,
        'form': form,
    })


@login_required
def getlist_equipment(request):
    paginator = Paginator(ModelEquipment.objects.all(), 20)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'reference_books/equipment_list.html', {
        'title': 'Списки оборудования',
        'list': list,
        'page': page,
    })


@login_required
@csrf_protect
def update_equipment(request, pk):
    form = EquipmentForm(request.POST or None, instance=pk and ModelEquipment.objects.get(id=pk))

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('rbooks:getlist_equipment')

    return render(request, 'reference_books/equipment_item.html', {
        'eq_id': pk,
        'form': form,
    })