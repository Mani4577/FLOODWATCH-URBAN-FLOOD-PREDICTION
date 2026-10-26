import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';

const HistoricalPage = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistorical = async () => {
      try {
        const res = await api.getHistorical();
        setEvents(res);
      } catch (err) {
        console.error('Failed to fetch historical data');
      } finally {
        setLoading(false);
      }
    };
    fetchHistorical();
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 bg-gray-100 min-h-screen">
        <h1 className="text-3xl font-bold mb-6">Historical Flood Events</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="space-y-4">
            {events.map((event) => (
              <div key={event.id} className="bg-white p-4 rounded-2xl shadow-lg">
                <h3 className="font-semibold">{event.event_name} ({event.year})</h3>
                <p>{event.description}</p>
                <p>Affected Areas: {event.affected_areas}</p>
                <p>Rainfall: {event.rainfall} mm</p>
                {event.image_url && <img src={`http://localhost:8003${event.image_url}`} alt="Event" className="mt-2 max-w-xs" />}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoricalPage;