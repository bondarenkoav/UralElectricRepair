__author__ = 'ipman'

from django.conf.urls import url

from repairshop.views import add_scopeshipment, add_shipment, add_charactequipment, scopeshipment_update, \
    scopeshipment_archive, \
    assign_performer, forchecking_disassembly, forchecking_faultdetection, forchecking_mechanics, forchecking_tests, \
    get_files, forchecking_poles, forchecking_completing, forchecking_assembly, add_comment_scopeshipment, \
    getlist_shipments, get_shipment, fill_tabs, \
    forchecking_sections, forchecking_inductor, forchecking_anchor, forchecking_shields, forchecking_spindle, \
    update_disassembly_tab, update_faultdetection_tab, update_mechanics_tab, update_tests_tab, update_storage_tab, \
    update_poles_tab, update_sections_tab, update_inductor_tab, update_anchor_tab, update_shields_tab, \
    update_spindle_tab, update_completing_tab, update_assembly_tab, update_investments_tab, \
    getlist_scopeshipment_archive

app_name = 'production'

urlpatterns = [
    # Редактирование данных о оборудовании в ремонте
    url(r'scopeshipment/(?P<pk>\d+)/update/', scopeshipment_update, name='scopeshipment-update'),
    # Архивный ремонтный номер
    url(r'scopeshipment/(?P<pk>\d+)/archive/', scopeshipment_archive, name='scopeshipment-archive'),

    # Редактирование вкладок
    url(r'scopeshipment-(?P<pk>\d+)/disassembly-update/', update_disassembly_tab, name='update-disassembly-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/faultdetection-update/', update_faultdetection_tab, name='update-faultdetection-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/mechanics-update/', update_mechanics_tab, name='update-mechanics-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/tests-update/', update_tests_tab, name='update-tests-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/storage-update/', update_storage_tab, name='update-storage-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/poles-update/', update_poles_tab, name='update-poles-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/sections-update/', update_sections_tab, name='update-sections-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/inductor-update/', update_inductor_tab, name='update-inductor-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/anchor-update/', update_anchor_tab, name='update-anchor-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/shields-update/', update_shields_tab, name='update-shields-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/spindle-update/', update_spindle_tab, name='update-spindle-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/completing-update/', update_completing_tab, name='update-completing-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/assembly-update/', update_assembly_tab, name='update-assembly-tab'),
    url(r'scopeshipment-(?P<pk>\d+)/investments-update/', update_investments_tab, name='update-investments-tab'),

    # Заполнение вкладок
    url(r'scopeshipment/(?P<pk>\d+)/filltabs/', fill_tabs, name='fill_tabs'),

    url(r'^shipment/(?P<shipment_id>\d+)/scopeshipment/$', add_scopeshipment, name='add-scopeshipment'),
    url(r'^shipment/(?P<shipment_id>\d+)/equipments/$', add_charactequipment, name='add-charactequipment'),

    # Назначить исполнителя
    url(r'^assign-performer/(?P<type>\w+)-(?P<pk>\d+)/$', assign_performer, name='assign-performer'),

    # На проверку
    url(r'^for-checking/disassembly-(?P<pk>\d+)/$', forchecking_disassembly, name='forchecking-disassembly'),
    url(r'^for-checking/faultdetection-(?P<pk>\d+)/$', forchecking_faultdetection, name='forchecking-faultdetection'),
    url(r'^for-checking/mechanics-(?P<pk>\d+)/$', forchecking_mechanics, name='forchecking-mechanics'),
    url(r'^for-checking/tests-(?P<pk>\d+)/$', forchecking_tests, name='forchecking-tests'),
    url(r'^for-checking/poles-(?P<pk>\d+)/$', forchecking_poles, name='forchecking-poles'),
    url(r'^for-checking/sections-(?P<pk>\d+)/$', forchecking_sections, name='forchecking-sections'),
    url(r'^for-checking/inductor-(?P<pk>\d+)/$', forchecking_inductor, name='forchecking-inductor'),
    url(r'^for-checking/anchor-(?P<pk>\d+)/$', forchecking_anchor, name='forchecking-anchor'),
    url(r'^for-checking/shields-(?P<pk>\d+)/$', forchecking_shields, name='forchecking-shields'),
    url(r'^for-checking/spindle-(?P<pk>\d+)/$', forchecking_spindle, name='forchecking-spindle'),
    url(r'^for-checking/completing-(?P<pk>\d+)/$', forchecking_completing, name='forchecking-completing'),
    url(r'^for-checking/assembly-(?P<pk>\d+)/$', forchecking_assembly, name='forchecking-assembly'),

    # Добавить комментарии
    url(r'scopeshipment/comment/(?P<pk>\d+)/$', add_comment_scopeshipment, name='add-scopeshipment-comment'),

    # Скачивание файла
    url(r'^get-file/(?P<type>\w+)-(?P<pk>\d+)/$', get_files, name='get-file'),

    # Архив ремонта
    url(r'^scopeshipment-archive/$', getlist_scopeshipment_archive, name='getlist-scopeshipment-archive'),

    url(r'^shipment-list/$', getlist_shipments, name='getlist-shipments'),
    url(r'^shipment/(?P<pk>\d+)/$', get_shipment, name='get-shipment'),
    url(r'^shipment/$', add_shipment, name='add-shipment'),
]