__author__ = 'ipman'

from django.conf.urls import url
from dashboard.views import index

app_name = 'dashboard'

urlpatterns = [
    # Самая первая страница
    url(r'^', index, name='index'),
]