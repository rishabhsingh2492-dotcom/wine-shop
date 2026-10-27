import axios from 'axios';
export const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export default axios.create({ baseURL: BASE });
export const errText = (e) => e.response?.data?.error || e.response?.data?.detail ||
  (e.response ? JSON.stringify(e.response.data) : 'Cannot reach the backend. Is Django running on port 8000?');
