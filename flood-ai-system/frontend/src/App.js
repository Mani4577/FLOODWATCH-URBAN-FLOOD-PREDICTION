import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import DashboardPage from './pages/DashboardPage';
import FloodMapPage from './pages/FloodMapPage';
import InsightsPage from './pages/InsightsPage';
import ReportPage from './pages/ReportPage';
import ProtectedRoute from './components/ProtectedRoute';
import RoadImpactPage from './pages/RoadImpactPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/flood-map" element={<ProtectedRoute><FloodMapPage /></ProtectedRoute>} />
        <Route path="/insights" element={<ProtectedRoute><InsightsPage /></ProtectedRoute>} />        
        <Route path="/report" element={<ProtectedRoute><ReportPage /></ProtectedRoute>} />
        <Route 
  path="/road-impact" 
  element={
    <ProtectedRoute>
      <RoadImpactPage />
    </ProtectedRoute>
  } 
/>
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;
