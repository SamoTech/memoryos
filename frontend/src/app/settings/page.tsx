'use client'
import { useState } from 'react'
import { Settings, Shield, Cpu, Trash2 } from 'lucide-react'

export default function SettingsPage() {
  const [provider, setProvider] = useState('ollama')
  const [autoSummarize, setAutoSummarize] = useState(true)

  return (
    <div className="space-y-8 max-w-2xl">
      <h1 className="text-2xl font-bold text-white flex items-center gap-2">
        <Settings size={24} /> Settings
      </h1>

      {/* LLM Provider */}
      <section className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
        <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2"><Cpu size={18} /> LLM Provider</h2>
        <div className="space-y-2">
          {['ollama', 'groq', 'openai'].map(p => (
            <label key={p} className="flex items-center gap-3 cursor-pointer">
              <input type="radio" name="provider" value={p} checked={provider === p} onChange={() => setProvider(p)} className="accent-indigo-500" />
              <span className="capitalize text-gray-200">{p}</span>
              {p === 'ollama' && <span className="text-xs text-green-400 bg-green-400/10 px-2 py-0.5 rounded-full">Recommended (local)</span>}
            </label>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
        <h2 className="text-lg font-semibold text-gray-100">Features</h2>
        <label className="flex items-center justify-between">
          <span className="text-gray-300">Auto-summarize memories</span>
          <input type="checkbox" checked={autoSummarize} onChange={e => setAutoSummarize(e.target.checked)} className="accent-indigo-500 w-5 h-5" />
        </label>
      </section>

      {/* Privacy */}
      <section className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
        <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2"><Shield size={18} /> Privacy & Storage</h2>
        <p className="text-sm text-gray-400">All data is stored locally at <code className="bg-gray-800 px-1.5 py-0.5 rounded text-indigo-300">~/.memoryos/</code>. Nothing is sent to external servers unless you configure an API key.</p>
      </section>

      {/* Danger zone */}
      <section className="bg-red-950/30 rounded-xl p-6 border border-red-900/50 space-y-4">
        <h2 className="text-lg font-semibold text-red-400 flex items-center gap-2"><Trash2 size={18} /> Danger Zone</h2>
        <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors">
          Forget All Memories
        </button>
      </section>
    </div>
  )
}
