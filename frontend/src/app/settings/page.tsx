'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function SettingsPage() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api.health().then(setHealth).catch(() => {});
  }, []);

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
        <h2 className="font-semibold text-gray-200">Server Status</h2>
        {health ? (
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-gray-400">Status</span><span className="text-green-400">{health.status}</span></div>
            <div className="flex justify-between"><span className="text-gray-400">Version</span><span>{health.version}</span></div>
            <div className="flex justify-between"><span className="text-gray-400">Data dir</span><span className="text-gray-300 font-mono text-xs">{health.data_dir}</span></div>
            <div className="flex justify-between"><span className="text-gray-400">Embeddings</span><span>{health.embedding_provider}</span></div>
            <div className="flex justify-between"><span className="text-gray-400">Summarizer</span><span>{health.summarizer_provider}</span></div>
          </div>
        ) : (
          <p className="text-red-400 text-sm">Server offline. Run: <code className="font-mono">memoryos start</code></p>
        )}
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
        <h2 className="font-semibold text-gray-200">Configuration</h2>
        <p className="text-sm text-gray-400">Edit <code className="text-indigo-400 font-mono">~/.memoryos/.env</code> to configure providers, models, and storage settings.</p>
        <div className="space-y-2 text-sm font-mono bg-gray-950 border border-gray-800 rounded-lg p-4 text-gray-400">
          <div>SUMMARIZER_PROVIDER=ollama</div>
          <div>OLLAMA_MODEL=llama3</div>
          <div>EMBEDDING_MODEL=all-MiniLM-L6-v2</div>
          <div>AUTO_SUMMARIZE=true</div>
          <div>DATA_RETENTION_DAYS=0</div>
        </div>
      </div>

      <div className="bg-red-950/30 border border-red-900/50 rounded-xl p-6 space-y-3">
        <h2 className="font-semibold text-red-400">Danger Zone</h2>
        <p className="text-sm text-gray-400">Forget all memories permanently. This cannot be undone.</p>
        <button
          onClick={() => {
            if (confirm('Are you sure? This will permanently delete ALL memories.')) {
              alert('Use CLI: memoryos forget --all');
            }
          }}
          className="px-4 py-2 bg-red-600/20 border border-red-700 text-red-400 rounded-lg text-sm hover:bg-red-600/30 transition"
        >
          Forget All Memories
        </button>
      </div>
    </div>
  );
}
