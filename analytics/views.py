from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from analytics.forms import FilterWorksForm
from repairshop.models import ScopeShipment, Shipment
from tasks.models import Tasks


@login_required
@csrf_protect
def works(request):
    result = {}
    form = FilterWorksForm(request.POST or None, user=request.user)

    if request.POST:
        if form.is_valid():
            startdate = datetime.strptime(request.POST['startdate'], '%Y-%m-%d')
            if request.POST['enddate']:
                enddate = datetime.strptime(request.POST['enddate'], '%Y-%m-%d')
            else:
                enddate = startdate

            filter_executor = request.POST.get('executor', None)
            filter_client = request.POST.get('client', None)
            filter_author = request.POST.get('author', None)
            filter_status = request.POST.get('status', None)
            filter_norangedate = request.POST.get('norangedate', False)

            if filter_norangedate:
                result = Tasks.objects.all()
            else:
                result = Tasks.objects.filter(date_limit__range=(startdate, enddate))
            if filter_executor:
                result = result.filter(executor=filter_executor)
            if filter_client:
                shipments = Shipment.objects.filter(client=filter_client)
                scope_shipments = ScopeShipment.objects.filter(shipment__in=shipments)
                result = result.filter(scopeshipment_id__in=scope_shipments)
            if filter_author:
                result = result.filter(author=filter_author)
            if filter_status:
                result = result.filter(status=filter_status)

    return render(request, 'analytics/works.html', {
        'form': form,
        'list': result
    })
