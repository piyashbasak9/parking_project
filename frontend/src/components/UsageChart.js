import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const UsageChart = ({ data }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Hourly Occupancy</h3>
      <LineChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="hour" tickFormatter={(str) => new Date(str).toLocaleTimeString([], { hour: '2-digit' })} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="occupied_count" stroke="#8884d8" />
      </LineChart>
    </div>
  );
};

export default UsageChart;