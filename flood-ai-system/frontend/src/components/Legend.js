import React from 'react';

const Legend = () => {
  return (
    <div className="bg-white/90 backdrop-blur-lg rounded-lg shadow-lg p-3 max-w-xs">
      <h4 className="text-sm font-semibold mb-2 text-gray-800">Flood Risk Legend</h4>
      <div className="space-y-1">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span className="text-sm text-gray-700">Low Risk</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-yellow-500 rounded"></div>
          <span className="text-sm text-gray-700">Medium Risk</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span className="text-sm text-gray-700">High Risk</span>
        </div>
      </div>
    </div>
  );
};

export default Legend;