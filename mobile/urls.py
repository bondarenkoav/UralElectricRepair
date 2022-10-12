from django.conf.urls import url

from mobile.views import appointedperformer_disassembly, appointedperformer_faultdetection, \
    appointedperformer_mechanics, appointedperformer_tests, appointedperformer_poles, appointedperformer_sections, \
    appointedperformer_inductor, appointedperformer_anchor, appointedperformer_shields, appointedperformer_spindle, \
    appointedperformer_completing, appointedperformer_assembly, getlist_tasks_mobile, getitem_task_mobile

__author__ = 'ipman'

app_name = 'mobile'

urlpatterns = [
    url(r'ap-disassembly/(?P<pk>\d+)/$', appointedperformer_disassembly, name='appointed-performer-disassembly'),
    url(r'ap-faultdetection/(?P<pk>\d+)/$', appointedperformer_faultdetection, name='appointed-performer-faultdetection'),
    url(r'ap-mechanics/(?P<pk>\d+)/$', appointedperformer_mechanics, name='appointed-performer-mechanics'),
    url(r'ap-tests/(?P<pk>\d+)/$', appointedperformer_tests, name='appointed-performer-tests'),

    url(r'ap-poles/(?P<pk>\d+)/$', appointedperformer_poles, name='appointed-performer-poles'),
    url(r'ap-sections/(?P<pk>\d+)/$', appointedperformer_sections, name='appointed-performer-sections'),
    url(r'ap-inductor/(?P<pk>\d+)/$', appointedperformer_inductor, name='appointed-performer-inductor'),
    url(r'ap-anchor/(?P<pk>\d+)/$', appointedperformer_anchor, name='appointed-performer-anchor'),
    url(r'ap-shields/(?P<pk>\d+)/$', appointedperformer_shields, name='appointed-performer-shields'),
    url(r'ap-spindle/(?P<pk>\d+)/$', appointedperformer_spindle, name='appointed-performer-spindle'),

    url(r'ap-completing/(?P<pk>\d+)/$', appointedperformer_completing, name='appointed-performer-completing'),
    url(r'ap-assembly/(?P<pk>\d+)/$', appointedperformer_assembly, name='appointed-performer-assembly'),

    url(r'^task-(?P<pk>\d+)/$', getitem_task_mobile, name='getitem_task'),

    url(r'', getlist_tasks_mobile, name='getlist-executor-tasks'),

]