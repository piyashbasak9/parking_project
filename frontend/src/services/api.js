import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const fetchSummary = (date) =>
  axios.get(`${API_BASE}/dashboard/summary/`, { params: { date } }).then(res => res.data);

export const fetchDevices = () =>
  axios.get(`${API_BASE}/devices/`).then(res => res.data);

export const fetchAlerts = () =>
  axios.get(`${API_BASE}/alerts/`).then(res => res.data);

export const fetchHourlyData = (zoneId, date) =>
  axios.get(`${API_BASE}/dashboard/hourly/`, { params: { zone: zoneId, date } }).then(res => res.data);