import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const LoginPage = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.login(form);
      localStorage.setItem('token', res.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 to-purple-600">
      <div className="bg-white/20 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-white text-center mb-6">Login</h2>
        {error && <p className="text-red-300 text-center mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            className="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white"
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            className="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white"
            required
          />
          <button
            type="submit"
            className="w-full bg-white text-blue-600 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-300"
          >
            Login
          </button>
        </form>
        <p className="text-white text-center mt-4">
          Don't have an account? <Link to="/signup" className="underline">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;