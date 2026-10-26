import React from 'react';

function FloodInfoPanel({ selectedCell }) {
  if (!selectedCell) {
    return <div className="info-panel">Click a zone to see details.</div>;
  }

  return (
    <div className="info-panel">
      <h3>Flood Cell Information</h3>
      <p><strong>Risk:</strong> {selectedCell.risk_level}</p>
      <p><strong>Probability:</strong> {selectedCell.flood_probability?.toFixed(2)}</p>
      <p><strong>Duration:</strong> {selectedCell.duration}</p>
      <p><strong>Main Causes:</strong></p>
      <pre>{selectedCell.causes}</pre>
    </div>
  );
}

export default FloodInfoPanel;
