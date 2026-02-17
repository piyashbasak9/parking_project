import React from 'react';

const ZoneTable = ({ zones }) => {
  return (
    <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse', width: '100%' }}>
      <thead>
        <tr>
          <th>Zone</th>
          <th>Current Occupancy</th>
          <th>Daily Target</th>
          <th>Actual Events</th>
          <th>Efficiency (%)</th>
          <th>Avg Health</th>
        </tr>
      </thead>
      <tbody>
        {zones.map((zone, idx) => (
          <tr key={idx}>
            <td>{zone.zone}</td>
            <td>{zone.current_occupancy}</td>
            <td>{zone.daily_target}</td>
            <td>{zone.actual_events}</td>
            <td>{zone.efficiency}</td>
            <td>{zone.avg_health}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ZoneTable;