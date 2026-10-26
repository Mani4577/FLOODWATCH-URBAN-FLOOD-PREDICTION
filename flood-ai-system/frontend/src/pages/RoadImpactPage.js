import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';

const RoadImpactPage = () => {
  const [roads, setRoads] = useState([]);
  const [locationName, setLocationName] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("lastFloodResult");

    if (saved) {
      const res = JSON.parse(saved);

      setLocationName(res.location?.address || "Selected Area");

      // ✅ USE SAME DATA (NO NEW API CALL)
      const roadData = res.road_impacts || [];

      setRoads(roadData);
    }
  }, []);

  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1 p-6">

        <h1 className="text-2xl font-bold mb-2">
          🚧 Road Impact Analysis
        </h1>

        <p className="text-gray-600 mb-6">{locationName}</p>

        {/* RESULTS */}
        <div className="grid gap-3">

          {roads.length === 0 ? (
            <p className="text-gray-500">No road data available</p>
          ) : (
            roads.map((r, i) => (
              <div
                key={i}
                className={`p-3 rounded text-white ${
                  r.risk_level === "RED"
                    ? "bg-red-500"
                    : r.risk_level === "YELLOW"
                    ? "bg-yellow-500 text-black"
                    : "bg-green-500"
                }`}
              >
                <b>{r.road_name}</b> → {r.risk_level}
              </div>
            ))
          )}

        </div>

      </div>
    </div>
  );
};

export default RoadImpactPage;