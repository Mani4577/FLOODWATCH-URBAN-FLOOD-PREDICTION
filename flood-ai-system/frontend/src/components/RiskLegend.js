import React from 'react';

function RiskLegend() {
  return (
    <div className="legend">
      <h4>Risk Legend</h4>
      <div><span className="legend-color green" />Low (GREEN)</div>
      <div><span className="legend-color yellow" />Medium (YELLOW)</div>
      <div><span className="legend-color red" />High (RED)</div>
    </div>
  );
}

export default RiskLegend;
