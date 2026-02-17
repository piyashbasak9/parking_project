import React from 'react';

const DeviceStatus = ({ devices }) => {
  return (
    <div>
      <h3>Device Status</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {devices.map(d => (
          <li key={d.code} style={{ margin: '5px 0', padding: '5px', border: '1px solid #ddd' }}>
            {d.code} ({d.zone}) – Last seen:{' '}
            {d.last_seen ? new Date(d.last_seen).toLocaleTimeString() : 'never'}
            <span style={{ marginLeft: '10px', fontWeight: 'bold', color: d.status === 'OK' ? 'green' : d.status === 'WARNING' ? 'orange' : 'red' }}>
              {d.status}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DeviceStatus;