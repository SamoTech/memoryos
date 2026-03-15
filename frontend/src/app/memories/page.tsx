'use client'
import { useState } from 'react'
import { useMemories } from '@/hooks/useMemories'
import { MemoryCard } from '@/components/MemoryCard'
import { Filter } from 'lucide-react'

const SOURCES = ['all', 'chatgpt', 'claude', 'gemini', 'cursor', 'manual', 'cli', 'api']

export default function MemoriesPage() {
  const [source, setSource] = useState<string | undefined>(undefined)
  const [pinnedOnly, setPinnedOnly] = useState(false)
  const { memories, isLoading } = useMemories({ source, pinnedOnly })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">All Memories</h1>
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-gray-400" />
          <select
            className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200"
            value={source ?? 'all'}
            onChange={e => setSource(e.target.value === 'all' ? undefined : e.target.value)}
          >
            {SOURCES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          <label className="flex items-center gap-1.5 text-sm text-gray-300 cursor-pointer">
            <input type="checkbox" checked={pinnedOnly} onChange={e => setPinnedOnly(e.target.checked)} className="accent-indigo-500" />
            Pinned only
          </label>
        </div>
      </div>

      {isLoading && <p className="text-gray-400 animate-pulse">Loading memories...</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {memories.map((m: any) => <MemoryCard key={m.id} memory={m} />)}
      </div>

      {!isLoading && memories.length === 0 && (
        <div className="text-center py-20 text-gray-500">
          <p className="text-5xl mb-4">🧠</p>
          <p>No memories yet. Install the browser extension to start capturing.</p>
        </div>
      )}
    </div>
  )
}
