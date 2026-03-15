'use client'
import { motion } from 'framer-motion'
import { Pin, Trash2, Brain, Clock } from 'lucide-react'
import { SourceBadge } from './SourceBadge'
import { api } from '@/lib/api'
import { useQueryClient } from '@tanstack/react-query'

interface Tag { id: string; name: string; color: string }
interface Memory {
  id: string; content: string; summary?: string; source: string
  is_pinned: boolean; importance_score: number; created_at: string
  tags: Tag[]; access_count: number
}

export function MemoryCard({ memory, score }: { memory: Memory; score?: number }) {
  const qc = useQueryClient()

  const handlePin = async () => {
    await api.post(`/api/v1/memories/${memory.id}/pin`)
    qc.invalidateQueries({ queryKey: ['memories'] })
  }

  const handleForget = async () => {
    if (!confirm('Forget this memory?')) return
    await api.delete(`/api/v1/memories/${memory.id}`)
    qc.invalidateQueries({ queryKey: ['memories'] })
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`bg-gray-900 border rounded-xl p-4 space-y-3 group hover:border-indigo-500/50 transition-colors ${
        memory.is_pinned ? 'border-indigo-500/40' : 'border-gray-800'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <SourceBadge source={memory.source} />
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button onClick={handlePin} className="p-1.5 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-indigo-400">
            <Pin size={14} className={memory.is_pinned ? 'text-indigo-400 fill-indigo-400' : ''} />
          </button>
          <button onClick={handleForget} className="p-1.5 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-red-400">
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {/* Summary or content */}
      <p className="text-gray-200 text-sm leading-relaxed line-clamp-4">
        {memory.summary || memory.content}
      </p>

      {/* Importance bar */}
      <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full"
          style={{ width: `${memory.importance_score * 100}%` }}
        />
      </div>

      {/* Tags */}
      {memory.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {memory.tags.slice(0, 5).map(tag => (
            <span key={tag.id} className="text-xs px-2 py-0.5 rounded-full text-white/80" style={{ backgroundColor: tag.color + '33', border: `1px solid ${tag.color}55` }}>
              {tag.name}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <Clock size={11} />
          {new Date(memory.created_at).toLocaleDateString()}
        </span>
        {score !== undefined && (
          <span className="flex items-center gap-1 text-indigo-400">
            <Brain size={11} /> {(score * 100).toFixed(0)}%
          </span>
        )}
      </div>
    </motion.div>
  )
}
