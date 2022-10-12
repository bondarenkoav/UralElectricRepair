from django.conf.urls import url

from analytics.views import works

__author__ = 'ipman'



app_name = 'rbooks'

urlpatterns = [
    url(r'^works/', works, name='report_works'),
    #url(r'^notbusy_work/', , name='report_notbusy work'),
]