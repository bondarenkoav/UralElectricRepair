from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from reference_books.models import Branches, Client, Posts, Parts, ModelEquipment, StatusWork, City, StageProduction, \
    Material, TreeTechProcess, TreeTechProcessStage


class ModelEquipmentAdmin(admin.ModelAdmin):
    model = ModelEquipment
    list_display = ['type', 'amperage', 'name', 'p', 'u', 'n', 'unn', 'uvn']


admin.site.register(TreeTechProcess, DraggableMPTTAdmin)
admin.site.register(TreeTechProcessStage, DraggableMPTTAdmin)
admin.site.register(Branches)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(Posts)
admin.site.register(Parts)
admin.site.register(ModelEquipment, ModelEquipmentAdmin)
admin.site.register(StatusWork)
admin.site.register(StageProduction)
admin.site.register(Material)
