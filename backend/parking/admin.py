from django.contrib import admin
from .models import Facility, Zone, Device, TelemetryData, ParkingLog, Alert, ZoneTarget

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'facility', 'description')
    list_filter = ('facility',)
    search_fields = ('name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'zone', 'is_active', 'installed_at')
    list_filter = ('zone', 'is_active')
    search_fields = ('code',)

@admin.register(TelemetryData)
class TelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'voltage', 'current', 'power_factor', 'timestamp', 'created_at')
    list_filter = ('device__zone',)
    search_fields = ('device__code',)
    date_hierarchy = 'timestamp'

@admin.register(ParkingLog)
class ParkingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'is_occupied', 'timestamp', 'created_at')
    list_filter = ('device__zone', 'is_occupied')
    search_fields = ('device__code',)
    date_hierarchy = 'timestamp'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'severity', 'message', 'is_acknowledged', 'created_at', 'resolved_at')
    list_filter = ('severity', 'is_acknowledged', 'device__zone')
    search_fields = ('message', 'device__code')
    date_hierarchy = 'created_at'

@admin.register(ZoneTarget)
class ZoneTargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'daily_target_occupancy', 'updated_at')
    list_filter = ('zone',)