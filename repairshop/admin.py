from django.contrib import admin

from repairshop.models import Shipment, ScopeShipment


class ScopeShipmentAdmin(admin.TabularInline):
    model = ScopeShipment
    extra = 0


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['specificationnum', 'branch', 'client', 'dateshipment']
    list_filter = ['branch', 'client', 'dateshipment']
    inlines = [ScopeShipmentAdmin]
    model = Shipment


admin.site.register(Shipment, ShipmentAdmin)
