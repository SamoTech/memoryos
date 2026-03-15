'use client'
import { motion } from 'framer-motion'
import { SourceBadge } from './SourceBadge'

export function SessionTimeline({ sessions }: { sessions: any[] }) {
  if (!sessions.length) {
    return (
      <div className="text-center py-20 text-gray-500">
        <p className="text-5xl mb-4">⏰</p>
        <p>No sessions recorded yet.</p>
      </div>
    )
  }

  return (
    <div className="relative pl-6 border-l border-gray-800 space-y-6">
      {sessions.map((s, i) => (
        <motion.div
          key={s.id}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.03 }}
          className="relative"
        >
          {/* Dot */}
          <div className="absolute -left-[1.65rem] top-3 w-3 h-3 rounded-full bg-indigo-500 border-2 border-gray-950" />

          <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-indigo-500/40 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <SourceBadge source={s.source} />
              <span className="text-xs text-gray-500">{new Date(s.started_at).toLocaleString()}</span>
            </div>
            <h3 className="font-medium text-gray-200">{s.title || 'Untitled session'}</h3>
            {s.summary && <p className="text-sm text-gray-400 mt-1">{s.summary}</p>}
            <p className="text-xs text-gray-600 mt-2">{s.memory_count} memories</p>
          </div>
        </motion.div>
      ))}
    </div>
  )
}
