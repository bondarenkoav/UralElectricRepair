__author__ = 'ipman'

from django.conf.urls import url

from reference_books.views import getlist_clients, update_client, update_clientforshipment, getlist_equipment, \
    update_equipment

app_name = 'rbooks'

urlpatterns = [
    url(r'^clients/(?P<client_id>\d+)/shipment/(?P<shipment_id>\d+)/', update_clientforshipment,
        name='update_clientforshipment'),
    url(r'^clients/(?P<pk>\d+)/', update_client, name='update_client'),
    url(r'^clients/$', getlist_clients, name='getlist_clients'),

    url(r'^equipments/(?P<pk>\d+)/', update_equipment, name='update_equipment'),
    url(r'^equipments/$', getlist_equipment, name='getlist_equipment'),
]