from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Menu

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(Menu, DraggableMPTTAdmin)
