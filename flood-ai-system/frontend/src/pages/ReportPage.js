import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';

const ReportPage = () => {
  const [form, setForm] = useState({
    location: '',
    latitude: '',
    longitude: '',
    description: '',
    water_level: '',
  });
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.keys(form).forEach(key => formData.append(key, form[key]));
    if (image) formData.append('image', image);

    try {
      await api.createReport(formData);
      setMessage('Report submitted successfully');
      setForm({ location: '', latitude: '', longitude: '', description: '', water_level: '' });
      setImage(null);
    } catch (err) {
      setMessage('Failed to submit report');
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 bg-gray-100 min-h-screen">
        <h1 className="text-3xl font-bold mb-6">Report Flood</h1>
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl shadow-lg space-y-4">
          <input
            type="text"
            name="location"
            placeholder="Location"
            value={form.location}
            onChange={handleChange}
            className="w-full p-3 border rounded"
            required
          />
          <input
            type="number"
            name="latitude"
            placeholder="Latitude"
            value={form.latitude}
            onChange={handleChange}
            className="w-full p-3 border rounded"
            step="any"
            required
          />
          <input
            type="number"
            name="longitude"
            placeholder="Longitude"
            value={form.longitude}
            onChange={handleChange}
            className="w-full p-3 border rounded"
            step="any"
            required
          />
          <textarea
            name="description"
            placeholder="Description"
            value={form.description}
            onChange={handleChange}
            className="w-full p-3 border rounded"
          />
          <input
            type="number"
            name="water_level"
            placeholder="Water Level"
            value={form.water_level}
            onChange={handleChange}
            className="w-full p-3 border rounded"
            step="any"
            required
          />
          <input
            type="file"
            onChange={handleFileChange}
            className="w-full p-3 border rounded"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700"
          >
            Submit Report
          </button>
        </form>
        {message && <p className="mt-4 text-center">{message}</p>}
      </div>
    </div>
  );
};

export default ReportPage;