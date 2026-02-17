import React from 'react';

const Filters = ({ date, setDate, zone, setZone }) => {
  return (
    <div style={{ marginBottom: '20px' }}>
      <label>Date: </label>
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <label style={{ marginLeft: '15px' }}>Zone: </label>
      <select value={zone} onChange={(e) => setZone(e.target.value)}>
        <option value="1">B1</option>
        <option value="2">VIP</option>
      </select>
    </div>
  );
};

export default Filters;