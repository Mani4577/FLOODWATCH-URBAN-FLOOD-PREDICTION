const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // ✅ FIX PORT

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export default {
  // ---------------- AUTH ----------------
  login: async (data) => {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },

  register: async (data) => {
    const res = await fetch(`${BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Registration failed');
    return res.json();
  },

  // ---------------- FLOOD PREDICTION ----------------
  floodPredict: async (data) => {
    const payload = {
      location: data.location,
      date: data.date || null, // ✅ important for historical
    };

    const res = await fetch(`${BASE_URL}/flood/predict`, { // ✅ FIXED ENDPOINT
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(), // optional if auth needed
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error('Prediction failed');
    return res.json();
  },

  // ---------------- ALERTS ----------------
  getAlerts: async () => {
    const res = await fetch(`${BASE_URL}/alerts/`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },

  // ---------------- REPORTS ----------------
  createReport: async (formData) => {
    const res = await fetch(`${BASE_URL}/reports/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to create report');
    return res.json();
  },

  // ---------------- HISTORICAL ----------------
  getHistorical: async () => {
    const res = await fetch(`${BASE_URL}/historical/`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch historical data');
    return res.json();
  },

  // ❌ REMOVE or keep only if needed (not used now)
  predict: async (data) => {
    const res = await fetch(`${BASE_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Prediction failed');
    return res.json();
  },
};