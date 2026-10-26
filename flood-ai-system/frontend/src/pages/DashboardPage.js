import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Sidebar from '../components/Sidebar';

const COLORS = {
  RED: '#ef4444',
  YELLOW: '#facc15',
  GREEN: '#22c55e',
};

const DashboardPage = () => {
  const [riskCounts, setRiskCounts] = useState({
    RED: 0,
    YELLOW: 0,
    GREEN: 0,
  });
  const [alerts, setAlerts] = useState([]);
  const [locationName, setLocationName] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("lastFloodResult");

    if (saved) {
      const res = JSON.parse(saved);

      const features = res.flood_map?.features || [];

      const counts = { RED: 0, YELLOW: 0, GREEN: 0 };

      features.forEach(f => {
        const risk = f.properties?.risk_level;
        if (counts[risk] !== undefined) counts[risk]++;
      });

      setRiskCounts(counts);
      setLocationName(res.location?.address || "Selected Area");

      // 🔥 SMART ALERTS
      const newAlerts = [];

      if (counts.RED > 0) {
        newAlerts.push({
          text: `High flood risk (${counts.RED} zones affected)`,
          type: "RED"
        });
      }

      if (counts.YELLOW > 5) {
        newAlerts.push({
          text: `Moderate flood risk detected`,
          type: "YELLOW"
        });
      }

      if (counts.GREEN > 0 && counts.RED === 0) {
        newAlerts.push({
          text: `Area mostly safe`,
          type: "GREEN"
        });
      }

      setAlerts(newAlerts);
    }
  }, []);

  const chartData = [
    { name: 'High Risk', value: riskCounts.RED, color: COLORS.RED },
    { name: 'Medium Risk', value: riskCounts.YELLOW, color: COLORS.YELLOW },
    { name: 'Low Risk', value: riskCounts.GREEN, color: COLORS.GREEN },
  ];

  const getCardStyle = (type) => {
    if (type === "RED") return "bg-red-50 border-red-200 text-red-600";
    if (type === "YELLOW") return "bg-yellow-50 border-yellow-200 text-yellow-600";
    return "bg-green-50 border-green-200 text-green-600";
  };

  return (
    <div className="flex bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <Sidebar />

      <div className="flex-1 p-6">

        {/* HEADER */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-5 rounded-2xl shadow-lg mb-6">
          <h1 className="text-2xl font-bold">📊 Flood Risk Dashboard</h1>
          <p className="text-sm opacity-90">{locationName}</p>
        </div>

        {/* CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">

          <div className="bg-white p-6 rounded-2xl shadow-lg hover:scale-105 transition">
            <h3 className="text-lg font-semibold text-gray-600">High Risk</h3>
            <p className="text-4xl font-bold text-red-600">{riskCounts.RED}</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg hover:scale-105 transition">
            <h3 className="text-lg font-semibold text-gray-600">Medium Risk</h3>
            <p className="text-4xl font-bold text-yellow-500">{riskCounts.YELLOW}</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg hover:scale-105 transition">
            <h3 className="text-lg font-semibold text-gray-600">Low Risk</h3>
            <p className="text-4xl font-bold text-green-600">{riskCounts.GREEN}</p>
          </div>

        </div>

        {/* CHART + ALERTS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* PIE CHART */}
          <div className="bg-white p-6 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">Risk Distribution</h3>

            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>

                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* ALERTS */}
          <div className="bg-white p-6 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">Smart Alerts</h3>

            {alerts.length === 0 ? (
              <p className="text-gray-500">No alerts</p>
            ) : (
              alerts.map((alert, idx) => (
                <div
                  key={idx}
                  className={`mb-3 p-3 rounded-lg border ${getCardStyle(alert.type)}`}
                >
                  {alert.text}
                </div>
              ))
            )}
          </div>

        </div>

      </div>
    </div>
  );
};

export default DashboardPage;