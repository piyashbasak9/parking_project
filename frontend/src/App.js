import React, { useState, useEffect } from 'react';
import DashboardSummary from './components/DashboardSummary';
import ZoneTable from './components/ZoneTable';
import DeviceStatus from './components/DeviceStatus';
import AlertPanel from './components/AlertPanel';
import UsageChart from './components/UsageChart';
import Filters from './components/Filters';
import { fetchSummary, fetchDevices, fetchAlerts, fetchHourlyData } from './services/api';
import './App.css';

function App() {
  const [summary, setSummary] = useState(null);
  const [devices, setDevices] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [hourlyData, setHourlyData] = useState([]);
  const [selectedZone, setSelectedZone] = useState('1');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, [date]);

  useEffect(() => {
    if (selectedZone) {
      fetchHourlyData(selectedZone, date).then(setHourlyData);
    }
  }, [selectedZone, date]);

  const loadData = async () => {
    const [summaryRes, devicesRes, alertsRes] = await Promise.all([
      fetchSummary(date),
      fetchDevices(),
      fetchAlerts(),
    ]);
    setSummary(summaryRes);
    setDevices(devicesRes);
    setAlerts(alertsRes);
  };

  const handleAcknowledge = async (alertId) => {
    await fetch(`http://localhost:8000/api/alerts/${alertId}/acknowledge/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
    });
    loadData();
  };

  if (!summary) return <div>Loading...</div>;

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>Smart Parking Monitor</h1>
      <Filters date={date} setDate={setDate} zone={selectedZone} setZone={setSelectedZone} />
      <DashboardSummary summary={summary} />
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px', flexWrap: 'wrap' }}>
        <ZoneTable zones={summary.zones} />
        <DeviceStatus devices={devices} />
      </div>
      <UsageChart data={hourlyData} />
      <AlertPanel alerts={alerts} onAcknowledge={handleAcknowledge} />
    </div>
  );
}

export default App;