import React from 'react';

const DashboardSummary = ({ summary }) => {
  return (
    <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', marginBottom: '20px' }}>
      <div className="card">Total Events: {summary.total_parking_events}</div>
      <div className="card">Current Occupancy: {summary.current_occupancy}</div>
      <div className="card">Active Devices: {summary.active_devices}</div>
      <div className="card">Alerts Today: {summary.alerts_today}</div>
    </div>
  );
};

export default DashboardSummary;