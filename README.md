### Smart Car Parking Monitoring & Alert System

### Complete Project Documentation

### 📋 Project Overview
This project is a Smart Car Parking Monitoring & Alert System built using Django (backend) and React (frontend). It simulates a real-world parking facility where multiple zones (e.g., B1, VIP) are equipped with devices that send telemetry (voltage, current, power factor) and occupancy data (slot free/occupied). The system ingests this data, applies business logic (device offline detection, abnormal power alerts, efficiency calculation, device health scoring), and presents a live monitoring dashboard.

### 🛠 Technology Stack
Layer	Technology
Backend	Django, Django REST Framework
Database	SQLite (default, easily changeable)
Frontend	React, Axios, Recharts
Other	CORS Headers, Django Filters


### 📁 Project Structure
``` bash
parking_project/
├── backend/
│   ├── parking_project/          # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── parking/                   # Main app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py               # Admin panel configuration
│   │   ├── models.py              # Database models
│   │   ├── serializers.py         # API serializers
│   │   ├── urls.py                 # API routing
│   │   ├── utils.py                # Business logic functions
│   │   └── views.py                # API view functions
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   └── initial_data.json           # Sample data fixture
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── DashboardSummary.js  # Summary cards component
    │   │   ├── ZoneTable.js         # Zone performance table component
    │   │   ├── DeviceStatus.js      # Device status list component
    │   │   ├── AlertPanel.js        # Alert panel component
    │   │   ├── UsageChart.js        # Hourly occupancy chart component
    │   │   └── Filters.js           # Date and zone filter component
    │   ├── services/
    │   │   └── api.js                # API call functions
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    ├── package.json
    └── README.md
```

### 🚀 Setup Instructions

# Prerequisites
```bash
Python 3.8+
Node.js 14+

pip (Python package manager)
npm (Node package manager)
```

# Backend Setup
``` bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
# On Windows: venv\Scripts\activate

# Install required packages
pip install django djangorestframework django-cors-headers django-filter

# Generate requirements.txt (if not present)
pip freeze > requirements.txt

# Create and apply database migrations
python manage.py makemigrations
python manage.py migrate

# Load sample data
python manage.py loaddata initial_data.json

# Create superuser (for admin panel)
python manage.py createsuperuser

# Start the server
python manage.py runserver
The backend will be available at http://localhost:8000.
```

## Frontend Setup
``` bash
# Open a new terminal and navigate to frontend folder
cd frontend

# Install required packages
npm install axios recharts

# Start the React development server
npm start
```
The frontend will open at http://localhost:3000.

Note: Ensure the backend is running before starting the frontend.


## ✅ Completed Features

1. Data Models (models.py)

# Facility
name: Name of the parking facility (e.g., "Main Parking")
location: Physical location (e.g., "Downtown")
Purpose: Identifies the overall parking site.

# Zone
facility: ForeignKey to Facility
name: Zone name (e.g., "B1", "VIP")
description: Optional description
Purpose: Represents different areas within a facility.

# Device
code: Unique device identifier (e.g., "PARK-B1-S001")
zone: ForeignKey to Zone
is_active: Boolean indicating if the device is currently active
installed_at: Auto-set installation timestamp
Purpose: Represents a device attached to a parking slot.

# TelemetryData
device: ForeignKey to Device
voltage: Float
current: Float
power_factor: Float
timestamp: DateTime when the data was recorded by the device
created_at: Auto-set server reception timestamp
Meta: unique_together = ['device', 'timestamp'] prevents duplicates
Purpose: Stores periodic electrical data from devices.

# ParkingLog
device: ForeignKey to Device
is_occupied: Boolean (True = occupied, False = free)
timestamp: DateTime of the occupancy change
created_at: Auto-set server reception timestamp
Meta: ordering = ['-timestamp']
Purpose: Logs when a slot becomes occupied or free.

# Alert
device: ForeignKey to Device (nullable)
severity: Choices: INFO, WARNING, CRITICAL
message: Text description
is_acknowledged: Boolean, whether user has acknowledged
created_at: Auto-set creation time
resolved_at: Nullable, set when acknowledged
Meta: ordering = ['-created_at']
Purpose: Stores system-generated alerts (offline, abnormal power, etc.).

# ZoneTarget
zone: OneToOneField to Zone
daily_target_occupancy: Integer – expected number of occupancy events per day
updated_at: Auto-updated timestamp
Purpose: Defines performance targets per zone.

## 2. API Endpoints (urls.py & views.py)

# Method	Endpoint	Description
POST	/api/telemetry/	Submit a single telemetry record
POST	/api/telemetry/bulk/	Submit multiple telemetry records
POST	/api/parking-log/	Submit an occupancy change
GET	/api/dashboard/summary/?date=YYYY-MM-DD	Get dashboard summary data
GET	/api/dashboard/hourly/?zone=<id>&date=YYYY-MM-DD	Get hourly occupancy for a zone
GET	/api/devices/	List active devices with last seen and status
GET	/api/alerts/	List alerts (filterable by severity, is_acknowledged)
PATCH	/api/alerts/<id>/acknowledge/	Mark an alert as acknowledged


## 3. Business Logic (utils.py)

# check_device_offline()
Purpose: Detects devices that haven't sent telemetry in the last 2 minutes.
Action: Creates a CRITICAL alert for each such device (duplicate prevention).

# check_abnormal_power(telemetry)
Purpose: Checks if voltage > 250 or current > 10.
Action: Creates a WARNING alert if abnormal (duplicate prevention).

# get_device_health(device)
Purpose: Calculates a health score (0–100) based on:
Number of alerts in the last 24 hours (each alert reduces score by 10)
Minutes since last telemetry (loses 2 points per minute)
Formula: (alert_score + recency_score) / 2
get_dashboard_summary(date_str)
Purpose: Returns summary data for a given date:
total_parking_events: Total ParkingLog entries for that day
current_occupancy: Count of devices whose last log shows occupied
active_devices: Devices with telemetry in the last 5 minutes
alerts_today: Alerts created on that day
zones: Array of zone details (current occupancy, target, actual events, efficiency, avg health)
get_hourly_usage(zone_id, date_str)
Purpose: Returns hourly counts of occupied slots for a zone on a given date (used for charts).

### 4. Frontend Components

# DashboardSummary.js
Displays summary cards: Total Events, Current Occupancy, Active Devices, Alerts Today.

# ZoneTable.js
Table showing zone-wise performance: Zone, Current Occupancy, Daily Target, Actual Events, Efficiency %, Avg Health.

# DeviceStatus.js
List of devices with their code, zone, last seen timestamp, and status (OK/WARNING/CRITICAL) with color coding.

# AlertPanel.js
List of alerts with severity, message, timestamp; filter by severity; acknowledge button.

# UsageChart.js
Line chart (Recharts) showing hourly occupancy for the selected zone and date.

# Filters.js
Date picker and zone selector; updates summary and chart accordingly.

# App.js
Main component that assembles everything, polls the backend every 10 seconds, and handles state.


### 5. Serializers (serializers.py)
TelemetrySerializer: Validates device_code (active device exists), timestamp, and enforces unique together.
ParkingLogSerializer: Validates device existence.
AlertSerializer: Serializes alert data with device code read-only.


### 6. Admin Panel (admin.py)
All models registered with custom list displays and filters for easy management.



### ❌ Incomplete Features
The following features were not implemented due to time constraints:
Excel/PDF export (only basic CSV download is present)
Advanced sorting/search in tables
User authentication and role-based access
WebSocket integration (real-time updates instead of polling)
Mobile-responsive design
Unit/integration tests
Email/SMS notifications for alerts



### ⚙️ Business Logic Assumptions & Thresholds

# Device Offline Detection
Threshold: 2 minutes (120 seconds)
Assumption: Devices are expected to send telemetry at least once every 2 minutes.
Alert Level: CRITICAL
Duplicate Prevention: Only one unresolved offline alert per device.

# Abnormal Power Usage
Voltage Threshold: > 250V (normal range 200–240V)
Current Threshold: > 10A (normal range 3–8A)
Alert Level: WARNING
Duplicate Prevention: Only one unresolved abnormal power alert per device.

# Device Health Score
Formula: (alert_score + recency_score) / 2
alert_score = max(0, 100 - (alerts_last_24h × 10))
recency_score = max(0, 100 - (minutes_since_last_telemetry × 2))
Range: 0–100 (integer)

# Device Status Indicators
OK: Last telemetry within 2 minutes
WARNING: Last telemetry 2–5 minutes ago
CRITICAL: Last telemetry >5 minutes ago or never

# Active Devices
Devices that have sent telemetry in the last 5 minutes.
Efficiency Calculation
Formula: (actual_events / daily_target) × 100%


### 🔮 Future Improvements (If More Time)

WebSocket Integration: Replace polling with Django Channels for real-time updates.
Excel/PDF Export: Use libraries like ReportLab or OpenPyXL.
Authentication: JWT or session-based login with role-based access.
Advanced Analytics: Predictive models for parking demand.
Mobile App: React Native for on-the-go monitoring.
Email/SMS Notifications: For critical alerts.
Machine Learning: Predict device failures.
Comprehensive Testing: Unit and integration tests.
Docker Deployment: Containerize the application.
CI/CD Pipeline: Automate testing and deployment.



### 📈 Scalability Thought Exercise

# Question: What changes would you make if this system had 5,000 devices sending data every 10 seconds?

# Answer:

Database Upgrade: Replace SQLite with PostgreSQL for better concurrency.
Connection Pooling: Use PgBouncer to manage many connections.
Indexing: Add indexes on frequently queried fields (timestamp, device_id, zone_id).
Asynchronous Processing: Introduce a message queue (RabbitMQ/Kafka) and Celery workers to handle data ingestion asynchronously.
Time-Series Database: Use TimescaleDB or InfluxDB for telemetry data.
Caching: Cache dashboard summaries in Redis with a short TTL.
Rate Limiting: Protect API endpoints with rate limiting.
Horizontal Scaling: Run multiple Django instances behind a load balancer.
Data Archival: Archive old data or use aggregated tables.
Real-Time Updates: Switch from polling to WebSockets for lower latency.
Health Score Optimization: Pre-compute health scores in a background job.
Monitoring: Implement Prometheus/Grafana for system monitoring.

### 📝 API Documentation (Detailed)

``` bash
1. POST /api/telemetry/

Request Body:

json    
{
  "device_code": "PARK-B1-S001",
  "voltage": 220.5,
  "current": 5.2,
  "power_factor": 0.92,
  "timestamp": "2026-02-18T10:30:00Z"
}
Response (201 Created):

json
{
  "id": 1,
  "device_code": "PARK-B1-S001",
  "voltage": 220.5,
  "current": 5.2,
  "power_factor": 0.92,
  "timestamp": "2026-02-18T10:30:00Z"
}
2. POST /api/telemetry/bulk/
Request Body: Array of telemetry objects (as above)
Response (207 Multi-Status):

json
{
  "success": [...],
  "errors": [...]
}
3. POST /api/parking-log/
Request Body:

json
{
  "device_code": "PARK-B1-S001",
  "is_occupied": true,
  "timestamp": "2026-02-18T10:45:00Z"
}
4. GET /api/dashboard/summary/?date=2026-02-18
Response:

json
{
  "total_parking_events": 45,
  "current_occupancy": 12,
  "active_devices": 8,
  "alerts_today": 2,
  "zones": [
    {
      "zone": "B1",
      "current_occupancy": 8,
      "daily_target": 50,
      "actual_events": 32,
      "efficiency": 64.0,
      "avg_health": 85
    },
    {
      "zone": "VIP",
      "current_occupancy": 4,
      "daily_target": 20,
      "actual_events": 13,
      "efficiency": 65.0,
      "avg_health": 92
    }
  ]
}
5. GET /api/dashboard/hourly/?zone=1&date=2026-02-18
Response:

json
[
  {"hour": "2026-02-18T09:00:00Z", "occupied_count": 5},
  {"hour": "2026-02-18T10:00:00Z", "occupied_count": 12},
  {"hour": "2026-02-18T11:00:00Z", "occupied_count": 18}
]
6. GET /api/devices/
Response:

json
[
  {
    "code": "PARK-B1-S001",
    "zone": "B1",
    "last_seen": "2026-02-18T10:30:00Z",
    "status": "OK"
  },
  {
    "code": "PARK-B1-S002",
    "zone": "B1",
    "last_seen": "2026-02-18T10:15:00Z",
    "status": "WARNING"
  }
]
7. GET /api/alerts/?severity=CRITICAL
Response:

json
[
  {
    "id": 1,
    "device_code": "PARK-B1-S002",
    "severity": "CRITICAL",
    "message": "Device PARK-B1-S002 offline (no data for >2 minutes)",
    "is_acknowledged": false,
    "created_at": "2026-02-18T10:20:00Z"
  }
]
8. PATCH /api/alerts/1/acknowledge/
Response:

json
{
  "status": "acknowledged"
}
🧪 How to Send Test Data
From Browser Console:
javascript
// Send telemetry
fetch('http://localhost:8000/api/telemetry/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    device_code: 'PARK-B1-S001',
    voltage: 220,
    current: 5,
    power_factor: 0.9,
    timestamp: new Date().toISOString()
  })
});

// Send parking log
fetch('http://localhost:8000/api/parking-log/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    device_code: 'PARK-B1-S001',
    is_occupied: true,
    timestamp: new Date().toISOString()
  })
});
```

### Using Postman:
URL: http://localhost:8000/api/telemetry/

Method: POST

Headers: Content-Type: application/json

Body: JSON as above

### 🔍 Key Features
Duplicate Data Prevention: Unique together constraint on device + timestamp.
Alert Duplication Prevention: No duplicate unresolved alerts for the same condition.
Device Health Score: 0–100 based on activity and alerts.
Efficiency Calculation: Target vs actual comparison.
Real-Time Updates: Polling every 10 seconds.
Alert Management: Acknowledge alerts via API.