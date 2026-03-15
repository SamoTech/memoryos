'use client'
import { useState } from 'react'
import { Download } from 'lucide-react'

export default function ExportPage() {
  const [format, setFormat] = useState('markdown')
  const [loading, setLoading] = useState(false)

  const handleExport = async () => {
    setLoading(true)
    try {
      const res = await fetch(`http://127.0.0.1:8765/api/v1/export?format=${format}`, { method: 'POST' })
      const blob = await res.blob()
      const ext = format === 'json' ? 'json' : format === 'csv' ? 'csv' : 'md'
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url; a.download = `memoryos-export.${ext}`; a.click()
      URL.revokeObjectURL(url)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 max-w-lg">
      <h1 className="text-2xl font-bold text-white">Export Memories</h1>
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
        <div className="space-y-2">
          <label className="text-sm text-gray-400">Export format</label>
          {['json', 'markdown', 'csv'].map(f => (
            <label key={f} className="flex items-center gap-3 cursor-pointer">
              <input type="radio" name="format" value={f} checked={format === f} onChange={() => setFormat(f)} className="accent-indigo-500" />
              <span className="capitalize text-gray-200">{f}</span>
            </label>
          ))}
        </div>
        <button
          onClick={handleExport}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white px-4 py-2.5 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          <Download size={16} />
          {loading ? 'Exporting...' : `Export as ${format.toUpperCase()}`}
        </button>
      </div>
    </div>
  )
}
