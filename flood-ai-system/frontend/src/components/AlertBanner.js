import React from 'react';

function AlertBanner({ alerts }) {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="alert-banner">
      {alerts.map((alert, idx) => (
        <div key={idx}>{alert}</div>
      ))}
    </div>
  );
}

export default AlertBanner;
