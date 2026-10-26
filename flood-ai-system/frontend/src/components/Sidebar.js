import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Map,
  Bell,
  FileText,
  Route,
  LogOut
} from 'lucide-react';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const menuItems = [
    { path: "/dashboard", name: "Dashboard", icon: <LayoutDashboard size={18} /> },
    { path: "/flood-map", name: "Flood Map", icon: <Map size={18} /> },
    { path: "/insights", name: "Insights", icon: <Bell size={18} /> },
    { path: "/report", name: "Report Flood", icon: <FileText size={18} /> },
    { path: "/road-impact", name: "Road Impact", icon: <Route size={18} /> },
  ];

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 text-white w-64 h-screen p-5 flex flex-col shadow-xl">

      {/* LOGO */}
      <h2 className="text-2xl font-bold mb-8 tracking-wide flex items-center gap-2">
        🌊 Flood Monitor
      </h2>

      {/* MENU */}
      <nav className="space-y-2 flex-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 py-2 px-4 rounded-lg transition-all duration-200
                ${
                  isActive
                    ? "bg-white text-gray-900 shadow-md"
                    : "hover:bg-white/10"
                }`}
            >
              {item.icon}
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* LOGOUT */}
      <button
        onClick={handleLogout}
        className="flex items-center justify-center gap-2 bg-red-500 py-2 rounded-lg hover:bg-red-600 transition"
      >
        <LogOut size={16} />
        Logout
      </button>

    </div>
  );
};

export default Sidebar;