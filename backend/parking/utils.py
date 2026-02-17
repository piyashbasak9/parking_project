from django.utils import timezone
from datetime import timedelta
from .models import Device, TelemetryData, Alert, ParkingLog, ZoneTarget, Zone
from django.db.models import Count, Q
from django.db.models.functions import TruncHour

def check_device_offline():
    """Create CRITICAL alerts for devices with no telemetry in last 2 minutes."""
    threshold = timezone.now() - timedelta(minutes=2)
    devices_without_recent = Device.objects.filter(
        is_active=True
    ).exclude(
        telemetry__timestamp__gt=threshold
    ).distinct()

    for device in devices_without_recent:
        if not Alert.objects.filter(
            device=device,
            severity='CRITICAL',
            message__icontains='offline',
            resolved_at__isnull=True
        ).exists():
            Alert.objects.create(
                device=device,
                severity='CRITICAL',
                message=f"Device {device.code} offline (no data for >2 minutes)."
            )

def check_abnormal_power(telemetry):
    """Check if telemetry indicates abnormal power usage."""
    if telemetry.voltage > 250 or telemetry.current > 10:
        if not Alert.objects.filter(
            device=telemetry.device,
            severity='WARNING',
            message__icontains='abnormal power',
            resolved_at__isnull=True
        ).exists():
            Alert.objects.create(
                device=telemetry.device,
                severity='WARNING',
                message=f"Abnormal power usage: V={telemetry.voltage}, I={telemetry.current}"
            )

def get_device_health(device):
    """Calculate health score 0-100 based on recent activity and alerts."""
    last_24h = timezone.now() - timedelta(hours=24)
    alert_count = device.alerts.filter(created_at__gt=last_24h).count()
    last_telemetry = device.telemetry.order_by('-timestamp').first()
    if not last_telemetry:
        return 0
    minutes_since = (timezone.now() - last_telemetry.timestamp).total_seconds() / 60.0
    alert_score = max(0, 100 - alert_count * 10)
    recency_score = max(0, 100 - minutes_since * 2)
    score = (alert_score + recency_score) / 2
    return max(0, min(100, int(score)))

def get_dashboard_summary(date_str):
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    total_events = ParkingLog.objects.filter(timestamp__range=[start_of_day, end_of_day]).count()

    devices = Device.objects.filter(is_active=True)
    current_occupied = 0
    for device in devices:
        last_log = device.parking_logs.order_by('-timestamp').first()
        if last_log and last_log.is_occupied:
            current_occupied += 1

    five_min_ago = timezone.now() - timedelta(minutes=5)
    active_devices = Device.objects.filter(telemetry__timestamp__gt=five_min_ago).distinct().count()

    alerts_today = Alert.objects.filter(created_at__range=[start_of_day, end_of_day]).count()

    zones = Zone.objects.all()
    zone_data = []
    for zone in zones:
        target_obj = ZoneTarget.objects.filter(zone=zone).first()
        target = target_obj.daily_target_occupancy if target_obj else 0
        actual = ParkingLog.objects.filter(
            device__zone=zone,
            timestamp__range=[start_of_day, end_of_day]
        ).count()
        efficiency = (actual / target * 100) if target > 0 else 0

        zone_occupied = 0
        for device in zone.devices.filter(is_active=True):
            last_log = device.parking_logs.order_by('-timestamp').first()
            if last_log and last_log.is_occupied:
                zone_occupied += 1

        health_scores = [get_device_health(d) for d in zone.devices.all()]
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0

        zone_data.append({
            'zone': zone.name,
            'current_occupancy': zone_occupied,
            'daily_target': target,
            'actual_events': actual,
            'efficiency': round(efficiency, 2),
            'avg_health': round(avg_health, 2)
        })

    return {
        'total_parking_events': total_events,
        'current_occupancy': current_occupied,
        'active_devices': active_devices,
        'alerts_today': alerts_today,
        'zones': zone_data,
    }

def get_hourly_usage(zone_id, date_str):
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date = timezone.now().date()
    start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
    end = start + timedelta(days=1)
    logs = ParkingLog.objects.filter(
        device__zone_id=zone_id,
        timestamp__range=[start, end]
    ).annotate(hour=TruncHour('timestamp')).values('hour').annotate(
        occupied_count=Count('id', filter=Q(is_occupied=True))
    ).order_by('hour')
    return logs