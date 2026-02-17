import React, { useState } from 'react';

const AlertPanel = ({ alerts, onAcknowledge }) => {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? alerts : alerts.filter(a => a.severity === filter);

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Alerts</h3>
      <select onChange={(e) => setFilter(e.target.value)} value={filter}>
        <option value="all">All</option>
        <option value="INFO">Info</option>
        <option value="WARNING">Warning</option>
        <option value="CRITICAL">Critical</option>
      </select>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {filtered.map(alert => (
          <li key={alert.id} style={{
            margin: '5px 0',
            padding: '8px',
            border: '1px solid #ccc',
            backgroundColor: alert.severity === 'CRITICAL' ? '#fdd' : alert.severity === 'WARNING' ? '#ffd' : '#dfd'
          }}>
            <strong>{alert.severity}</strong> – {alert.message} – {new Date(alert.created_at).toLocaleString()}
            {!alert.is_acknowledged && (
              <button onClick={() => onAcknowledge(alert.id)} style={{ marginLeft: '10px' }}>
                Acknowledge
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AlertPanel;