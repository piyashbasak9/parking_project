from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name




class Zone(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.facility.name} - {self.name}"





class Device(models.Model):
    code = models.CharField(max_length=50, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='devices')
    is_active = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code





class TelemetryData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetry')
    voltage = models.FloatField()
    current = models.FloatField()
    power_factor = models.FloatField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['device', 'timestamp']





class ParkingLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='parking_logs')
    is_occupied = models.BooleanField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']





class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    message = models.TextField()
    is_acknowledged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']





class ZoneTarget(models.Model):
    zone = models.OneToOneField(Zone, on_delete=models.CASCADE, related_name='target')
    daily_target_occupancy = models.IntegerField(help_text="Expected number of occupancy events per day")
    updated_at = models.DateTimeField(auto_now=True)