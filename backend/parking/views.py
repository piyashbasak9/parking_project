from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Device, TelemetryData, ParkingLog, Alert, Zone, ZoneTarget
from .serializers import TelemetrySerializer, ParkingLogSerializer, AlertSerializer, ZoneTargetSerializer
from .utils import check_abnormal_power, get_dashboard_summary, get_hourly_usage

@api_view(['POST'])
def telemetry_create(request):
    serializer = TelemetrySerializer(data=request.data)
    if serializer.is_valid():
        telemetry = serializer.save()
        check_abnormal_power(telemetry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def telemetry_bulk(request):
    data = request.data
    if not isinstance(data, list):
        return Response({"error": "Expected a list of telemetry records."}, status=status.HTTP_400_BAD_REQUEST)
    results = []
    errors = []
    for idx, item in enumerate(data):
        serializer = TelemetrySerializer(data=item)
        if serializer.is_valid():
            telemetry = serializer.save()
            check_abnormal_power(telemetry)
            results.append(serializer.data)
        else:
            errors.append({"index": idx, "errors": serializer.errors})
    response = {"success": results, "errors": errors}
    status_code = status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED
    return Response(response, status=status_code)

@api_view(['POST'])
def parking_log_create(request):
    serializer = ParkingLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_summary(request):
    date = request.query_params.get('date')
    summary = get_dashboard_summary(date)
    return Response(summary)

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filterset_fields = ['severity', 'is_acknowledged']

    @action(detail=True, methods=['patch'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.is_acknowledged = True
        alert.resolved_at = timezone.now()
        alert.save()
        return Response({'status': 'acknowledged'})

@api_view(['GET'])
def hourly_usage(request):
    zone_id = request.query_params.get('zone')
    date = request.query_params.get('date')
    if not zone_id:
        return Response({"error": "zone parameter required"}, status=400)
    data = get_hourly_usage(zone_id, date)
    return Response(data)

@api_view(['GET'])
def devices(request):
    devices = Device.objects.filter(is_active=True).select_related('zone')
    data = []
    for d in devices:
        last_telemetry = d.telemetry.order_by('-timestamp').first()
        last_seen = last_telemetry.timestamp if last_telemetry else None
        if last_seen and (timezone.now() - last_seen).total_seconds() < 120:
            status_indicator = 'OK'
        elif last_seen and (timezone.now() - last_seen).total_seconds() < 300:
            status_indicator = 'WARNING'
        else:
            status_indicator = 'CRITICAL'
        data.append({
            'code': d.code,
            'zone': d.zone.name,
            'last_seen': last_seen,
            'status': status_indicator,
        })
    return Response(data)