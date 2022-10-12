from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from accounts.views import user_profile
from dashboard.views import logout
from repairshop.views import getlist_transformers, getlist_engines_variable, getlist_engines_steady, \
    getlist_engines_upto100kW, save_client

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    url(r'^schedule/', include('schedule.urls')),
    url(r'^fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    url(r'^scrumboard/', include('django_scrumboard.urls')),

    url(r'^accounts/logout/$', logout, name="logout"),
    url(r'^accounts/userprofile/$', user_profile, name='profile'),

    url(r'^ajax_add_client/', save_client, name='ajax_add_client'),

    url(r'transformers/', getlist_transformers, name='transformers'),
    url(r'engines/variable/', getlist_engines_variable, name='engines-variable'),
    url(r'engines/steady/', getlist_engines_steady, name='engines-steady'),
    url(r'engines/upto100kW/', getlist_engines_upto100kW, name='engines-upto100kW'),

    url(r'production/', include('repairshop.urls', namespace='production')),
    url(r'mobile/', include('mobile.urls', namespace='mobile')),
    url(r'rbooks/', include('reference_books.urls', namespace='rbooks')),
    url(r'tasks/', include('tasks.urls', namespace='tasks')),
    url(r'^analytics/', include('analytics.urls', namespace='analytics')),

    url(r'^', include('dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
