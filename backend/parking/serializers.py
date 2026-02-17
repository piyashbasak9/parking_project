from rest_framework import serializers
from .models import Facility, Zone, Device, TelemetryData, ParkingLog, Alert, ZoneTarget

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'




class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'




class DeviceSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    class Meta:
        model = Device
        fields = ['id', 'code', 'zone', 'zone_name', 'is_active', 'installed_at']





class TelemetrySerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(write_only=True)

    class Meta:
        model = TelemetryData
        fields = ['id', 'device_code', 'voltage', 'current', 'power_factor', 'timestamp']
        extra_kwargs = {
            'timestamp': {'required': True}
        }





    def validate_device_code(self, value):
        try:
            device = Device.objects.get(code=value, is_active=True)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Device not found or inactive.")
        return device





    def create(self, validated_data):
        device = validated_data.pop('device_code')
        return TelemetryData.objects.create(device=device, **validated_data)





class ParkingLogSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(write_only=True)

    class Meta:
        model = ParkingLog
        fields = ['id', 'device_code', 'is_occupied', 'timestamp']

    def validate_device_code(self, value):
        try:
            device = Device.objects.get(code=value, is_active=True)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Device not found or inactive.")
        return device

    def create(self, validated_data):
        device = validated_data.pop('device_code')
        return ParkingLog.objects.create(device=device, **validated_data)






class AlertSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(source='device.code', read_only=True)
    class Meta:
        model = Alert
        fields = ['id', 'device_code', 'severity', 'message', 'is_acknowledged', 'created_at', 'resolved_at']






class ZoneTargetSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    class Meta:
        model = ZoneTarget
        fields = ['id', 'zone', 'zone_name', 'daily_target_occupancy', 'updated_at']