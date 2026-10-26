import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import SearchBar from '../components/SearchBar';
import MapView from '../components/MapView';
import AlertBanner from '../components/AlertBanner';
import api from '../services/api';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const FloodMapPage = () => {
  const [location, setLocation] = useState(null);
  const [floodData, setFloodData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [selectedCellId, setSelectedCellId] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const [date, setDate] = useState("");
  const [mode, setMode] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [explanations, setExplanations] = useState([]);

  const handleSearch = async (place) => {
    setError(null);
    setLoading(true);
    setSelectedCell(null);
    setSelectedCellId(null);

    try {
      const res = await api.floodPredict({
        location: place,
        date: date
      });

      setLocation(res.location);
      setFloodData(res.flood_map);
      setAlerts(res.alerts);

      setMode(res.mode);
      setSelectedDate(res.selected_date);

      setExplanations(res.explanations || []);
      localStorage.setItem("lastFloodResult", JSON.stringify(res));

    } catch (err) {
      setError(err?.message || 'Network Error');
      setFloodData(null);
      setAlerts([]);
      setLocation(null);
    } finally {
      setLoading(false);
    }
  };

  const onSelectCell = (cell) => {
    setSelectedCell(cell);
    setSelectedCellId(cell.id);
  };

  const getRiskColor = (risk) => {
    if (risk === "RED") return "text-red-600";
    if (risk === "YELLOW") return "text-yellow-500";
    return "text-green-600";
  };

  const getCardBg = (risk) => {
    if (risk === "RED") return "bg-red-50 border-red-200";
    if (risk === "YELLOW") return "bg-yellow-50 border-yellow-200";
    return "bg-green-50 border-green-200";
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100 font-sans">
      <Sidebar />

      <div className="flex-1 flex flex-col p-6 gap-4">

        {/* HEADER */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-5 rounded-2xl shadow-lg">
          <h1 className="text-2xl font-bold">🌊 AI Flood Risk Monitoring</h1>
          <p className="text-sm opacity-90">
            Real-time flood prediction with AI & GIS
          </p>
        </div>

        {/* SEARCH */}
        <div className="bg-white/70 backdrop-blur-lg p-4 rounded-2xl shadow-md">
          <div className="flex items-center gap-3">
            <SearchBar onSearch={handleSearch} />

            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="border p-2 rounded-lg"
            />
          </div>

          {mode && (
            <div className="mt-2 text-sm text-gray-700">
              <p><b>Mode:</b> {mode}</p>
              {selectedDate && <p><b>Date:</b> {selectedDate}</p>}
            </div>
          )}

          {loading && <p className="text-blue-600 mt-2">Analyzing data...</p>}
          {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>

        {/* MAIN */}
        <div className="flex gap-4 flex-1 overflow-hidden">

          {/* MAP */}
          <div className="flex-[2] h-full rounded-2xl overflow-hidden shadow-lg">
            <MapView
              location={location}
              floodData={floodData}
              explanations={explanations}
              onSelectCell={onSelectCell}
              selectedCellId={selectedCellId}
              loading={loading}
            />
          </div>

          {/* RIGHT PANEL */}
          <div className="flex-1 overflow-y-auto space-y-4">

            <h3 className="text-lg font-semibold text-gray-800">
              Flood Insights
            </h3>

            {selectedCell ? (
              <>
                {/* 🔥 RISK CARD */}
                <div className={`p-4 rounded-2xl border shadow-sm ${getCardBg(selectedCell.risk_level)}`}>
                  <h2 className={`text-xl font-bold ${getRiskColor(selectedCell.risk_level)}`}>
                    {selectedCell.risk_level} RISK
                  </h2>
                  <p className="text-sm text-gray-600">
                    Probability: {selectedCell.flood_probability}
                  </p>
                  <p className="text-sm text-gray-600">
                    Duration: {selectedCell.duration}
                  </p>
                </div>

                {/* 📊 SHAP CHART */}
                <div className="bg-white p-4 rounded-2xl shadow-md">
                  <h4 className="font-semibold mb-2">
                    AI Explanation (Main Causes)
                  </h4>

                  {selectedCell.main_causes?.length > 0 ? (
                    <div className="h-60">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          layout="vertical"
                          data={selectedCell.main_causes
                            .sort((a, b) => b.importance_pct - a.importance_pct)
                            .map(c => ({
                              name: c.feature,
                              value: Number(c.importance_pct || 0)
                            }))
                          }
                        >
                          <XAxis type="number" />
                          <YAxis type="category" dataKey="name" width={120} />
                          <Tooltip />
                          <Bar dataKey="value" fill="#3b82f6" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No causes available</p>
                  )}
                </div>

              </>
            ) : (
              <div className="bg-white p-6 rounded-2xl shadow-md text-center text-gray-500">
                🔍 Click a grid cell to view flood details
              </div>
            )}

            {/* ALERTS */}
            <div className="bg-white p-4 rounded-2xl shadow-md">
              <h4 className="font-semibold mb-2">Alerts</h4>
              <AlertBanner alerts={alerts} />
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default FloodMapPage;