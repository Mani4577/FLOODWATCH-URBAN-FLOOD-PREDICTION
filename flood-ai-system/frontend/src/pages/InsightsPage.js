import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, ResponsiveContainer
} from 'recharts';

const COLORS = {
  RED: '#ef4444',
  YELLOW: '#facc15',
  GREEN: '#22c55e',
};

const InsightsPage = () => {
  const [rainfall, setRainfall] = useState([]);
  const [riskCounts, setRiskCounts] = useState({ RED: 0, YELLOW: 0, GREEN: 0 });
  const [locationName, setLocationName] = useState("");
  const [timeline, setTimeline] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem("lastFloodResult");
    if (!saved) return;

    const res = JSON.parse(saved);

    const features = res.flood_map?.features || [];
    const rain = res.rainfall || {};

    setLocationName(res.location?.address || "Selected Area");

    // ✅ COUNT RISKS
    const counts = { RED: 0, YELLOW: 0, GREEN: 0 };
    features.forEach(f => {
      const risk = f.properties?.risk_level;
      if (counts[risk] !== undefined) counts[risk]++;
    });
    setRiskCounts(counts);

    // ✅ RAIN DATA
    const rainArray = [
      rain.current || 0,
      rain.day_3 || 0,
      rain.day_7 || 0,
      rain.day_14 || 0,
    ];
    setRainfall(rainArray);

    // ✅ DYNAMIC TIMELINE (FIXED)
    let overall = "GREEN";
    if (counts.RED > 0) overall = "RED";
    else if (counts.YELLOW > 0) overall = "YELLOW";

    let timelineData = [];

    if (overall === "RED") {
      timelineData = [
        { day: "Today", risk: "RED" },
        { day: "3 Day", risk: "RED" },
        { day: "7 Day", risk: "YELLOW" },
        { day: "14 Day", risk: "GREEN" },
      ];
    } else if (overall === "YELLOW") {
      timelineData = [
        { day: "Today", risk: "YELLOW" },
        { day: "3 Day", risk: "YELLOW" },
        { day: "7 Day", risk: "GREEN" },
        { day: "14 Day", risk: "GREEN" },
      ];
    } else {
      timelineData = [
        { day: "Today", risk: "GREEN" },
        { day: "3 Day", risk: "GREEN" },
        { day: "7 Day", risk: "GREEN" },
        { day: "14 Day", risk: "GREEN" },
      ];
    }

    setTimeline(timelineData);

  }, []);

  // ✅ GRAPH DATA
  const chartData = [
    { name: "Today", rainfall: rainfall[0] || 0, risk: 1 },
    { name: "3 Day", rainfall: rainfall[1] || 0, risk: 2 },
    { name: "7 Day", rainfall: rainfall[2] || 0, risk: 3 },
    { name: "14 Day", rainfall: rainfall[3] || 0, risk: 4 },
  ];

  const comparisonData = [
    {
      name: "Rainfall",
      historical: rainfall[0] || 0,
      predicted: rainfall[2] || 0,
    },
    {
      name: "Flood Risk",
      historical: riskCounts.YELLOW,
      predicted: riskCounts.RED,
    },
  ];

  // ✅ ALERTS
  const smartAlerts = [];

  if (riskCounts.RED > 0) {
    smartAlerts.push(`🚨 High flood risk (${riskCounts.RED} zones affected)`);
  }

  if ((rainfall[0] || 0) > 50) {
    smartAlerts.push(`🌧 Heavy rainfall detected`);
  }

  if (riskCounts.GREEN > 0 && riskCounts.RED === 0) {
    smartAlerts.push(`✅ Area mostly safe`);
  }

  return (
    <div className="flex bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <Sidebar />

      <div className="flex-1 p-6">

        {/* HEADER */}
        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white p-5 rounded-2xl shadow-lg mb-6">
          <h1 className="text-2xl font-bold">📊 Insights & Analysis</h1>
          <p className="text-sm opacity-90">{locationName}</p>
        </div>

        {/* 📈 LINE CHART */}
        <div className="bg-white p-6 rounded-2xl shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-4">
            Rainfall vs Flood Risk Trend
          </h3>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" domain={[0, 5]} />
              <Tooltip />
              <Legend />

              <Line
                yAxisId="left"
                type="monotone"
                dataKey="rainfall"
                stroke="#3b82f6"
                strokeWidth={3}
                name="Rainfall (mm)"
              />

              <Line
                yAxisId="right"
                type="monotone"
                dataKey="risk"
                stroke="#ef4444"
                strokeWidth={3}
                name="Flood Risk Index"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* 📊 BAR CHART */}
        <div className="bg-white p-6 rounded-2xl shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-4">
            Historical vs Predicted Comparison
          </h3>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />

              <Bar dataKey="historical" fill="#3b82f6" name="Historical" />
              <Bar dataKey="predicted" fill="#ef4444" name="Predicted" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 📅 TIMELINE */}
        <div className="bg-white p-6 rounded-2xl shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-4">Risk Timeline</h3>

          <div className="flex gap-4">
            {timeline.map((t, i) => (
              <div key={i} className="flex-1 text-center">
                <div
                  className={`h-4 rounded ${
                    t.risk === "RED"
                      ? "bg-red-500"
                      : t.risk === "YELLOW"
                      ? "bg-yellow-400"
                      : "bg-green-500"
                  }`}
                />
                <p className="mt-2 text-sm font-semibold">{t.day}</p>
                <p className="text-xs text-gray-500">{t.risk}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 🚨 ALERTS */}
        <div className="bg-white p-6 rounded-2xl shadow-lg">
          <h3 className="text-lg font-semibold mb-4">Smart Alerts</h3>

          {smartAlerts.length === 0 ? (
            <p className="text-gray-500">No alerts</p>
          ) : (
            smartAlerts.map((alert, idx) => (
              <div
                key={idx}
                className="mb-3 p-3 rounded-lg bg-gray-100 border"
              >
                {alert}
              </div>
            ))
          )}
        </div>

      </div>
    </div>
  );
};

export default InsightsPage;