import React, { useMemo } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const riskColors = {
  GREEN: '#22c55e',
  YELLOW: '#facc15',
  RED: '#ef4444',
};

function getRiskStyle(risk, selected = false) {
  return {
    color: riskColors[risk] || '#22c55e',
    fillColor: riskColors[risk] || '#22c55e',
    fillOpacity: selected ? 0.9 : 0.6,
    weight: selected ? 3 : 1,
    opacity: 1,
  };
}

function MapView({ location, floodData, explanations, onSelectCell, selectedCellId, loading }) {

  const center = location
    ? [location.latitude, location.longitude]
    : [13.0827, 80.2707];

  // ✅ CREATE EXPLANATION MAP
  const explanationMap = useMemo(() => {
    const map = {};
    (explanations || []).forEach(e => {
      map[e.id] = e;
    });
    return map;
  }, [explanations]);

  const onEachFeature = (feature, layer) => {
    const props = feature?.properties || {};
    const gridId = props.grid_id;

    const explanation = explanationMap[gridId] || {};

    const risk = explanation.risk_level || props.risk_level;
    const prob = Number(explanation.probability || props.flood_probability || 0).toFixed(2);
    const duration = explanation.duration || props.duration;

    const causes = explanation.main_causes || [];

    let causeMarkup = 'No causes available';
    if (causes.length > 0) {
      causeMarkup = causes
        .map(c => `• ${c.feature} (${c.importance_pct}%)`)
        .join('<br/>');
    }

    layer.bindPopup(`
      <div style="font-family: Inter; padding:8px;">
        <h3>Flood Cell</h3>
        <p><b>Risk:</b> ${risk}</p>
        <p><b>Probability:</b> ${prob}</p>
        <p><b>Duration:</b> ${duration}</p>
        <b>Main Causes:</b><br/>
        ${causeMarkup}
      </div>
    `);

    layer.on({
      click: () => {
        onSelectCell({
          id: gridId,
          risk_level: risk,
          flood_probability: prob,
          duration: duration,
          main_causes: causes
        });
      }
    });
  };

  const styleFn = useMemo(
    () => (feature) => {
      const id = feature.properties?.grid_id;
      const selected = selectedCellId && id === selectedCellId;
      return getRiskStyle(feature?.properties?.risk_level, selected);
    },
    [selectedCellId]
  );

  return (
    <div className="h-full w-full relative">

      {loading && <div className="loading-overlay">Loading...</div>}

      <MapContainer center={center} zoom={13} style={{ height: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {location && <Marker position={center} />}

        {floodData && (
          <GeoJSON
            data={floodData}
            style={styleFn}
            onEachFeature={onEachFeature}
          />
        )}
      </MapContainer>
    </div>
  );
}

export default MapView;
