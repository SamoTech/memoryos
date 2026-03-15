'use client';
import { useState } from 'react';

const FORMATS = ['json', 'markdown', 'csv', 'obsidian'];
const SOURCES = ['all', 'chatgpt', 'claude', 'gemini', 'cursor', 'manual', 'cli', 'api'];

export default function ExportPage() {
  const [format, setFormat] = useState('markdown');
  const [source, setSource] = useState('all');

  const handleExport = () => {
    const params = new URLSearchParams({ format });
    if (source !== 'all') params.set('source', source);
    window.open(`http://localhost:8765/api/v1/export?${params.toString()}`);
  };

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Export Memories</h1>
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-5">
        <div>
          <label className="text-sm text-gray-400 block mb-2">Format</label>
          <div className="flex flex-wrap gap-2">
            {FORMATS.map((f) => (
              <button key={f} onClick={() => setFormat(f)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  format === f ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}>{f}</button>
            ))}
          </div>
        </div>
        <div>
          <label className="text-sm text-gray-400 block mb-2">Source filter</label>
          <div className="flex flex-wrap gap-2">
            {SOURCES.map((s) => (
              <button key={s} onClick={() => setSource(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                  source === s ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}>{s}</button>
            ))}
          </div>
        </div>
        <button
          onClick={handleExport}
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 rounded-xl font-medium transition"
        >
          ⬇ Download Export
        </button>
      </div>
    </div>
  );
}
