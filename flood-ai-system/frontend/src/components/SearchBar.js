import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const submit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query.trim());
  };

  return (
    <form onSubmit={submit} className="flex gap-3 items-center">
      <input
        className="flex-1 px-4 py-3 rounded-xl border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter location (e.g., Velachery Chennai)"
      />

      <button
        type="submit"
        className="px-5 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-blue-500 to-indigo-600 hover:scale-105 transition"
      >
        Predict
      </button>
    </form>
  );
}

export default SearchBar;
