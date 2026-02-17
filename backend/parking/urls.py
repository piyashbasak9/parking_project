from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'alerts', views.AlertViewSet)

urlpatterns = [
    path('telemetry/', views.telemetry_create, name='telemetry-create'),
    path('telemetry/bulk/', views.telemetry_bulk, name='telemetry-bulk'),
    path('parking-log/', views.parking_log_create, name='parking-log-create'),
    path('dashboard/summary/', views.dashboard_summary, name='dashboard-summary'),
    path('dashboard/hourly/', views.hourly_usage, name='hourly-usage'),
    path('devices/', views.devices, name='devices'),
    path('', include(router.urls)),
]