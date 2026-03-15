'use client'
import { useQuery } from '@tanstack/react-query'
import { Brain, Clock, Pin, Database, Zap } from 'lucide-react'
import { MemoryCard } from '@/components/MemoryCard'
import { StatsWidget } from '@/components/StatsWidget'
import { SearchBar } from '@/components/SearchBar'
import { api } from '@/lib/api'

export default function DashboardPage() {
  const { data: stats } = useQuery({ queryKey: ['stats'], queryFn: () => api.get('/api/v1/stats') })
  const { data: memories = [] } = useQuery({
    queryKey: ['memories', 'recent'],
    queryFn: () => api.get('/api/v1/memories?limit=20'),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Brain className="text-indigo-400" size={28} />
          MemoryOS
        </h1>
        <p className="text-gray-400 text-sm mt-1">Your AI finally remembers you.</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsWidget label="Total Memories" value={stats?.total_memories ?? '—'} icon={<Brain size={16} />} color="indigo" />
        <StatsWidget label="Sessions" value={stats?.total_sessions ?? '—'} icon={<Clock size={16} />} color="violet" />
        <StatsWidget label="Pinned" value={stats?.pinned_memories ?? '—'} icon={<Pin size={16} />} color="emerald" />
        <StatsWidget label="DB Size" value={stats ? `${stats.db_size_mb} MB` : '—'} icon={<Database size={16} />} color="amber" />
      </div>

      {/* Quick search */}
      <SearchBar />

      {/* Recent memories */}
      <div>
        <h2 className="text-lg font-semibold text-gray-200 mb-3 flex items-center gap-2">
          <Zap size={18} className="text-yellow-400" /> Recent Memories
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {memories.map((m: any) => (
            <MemoryCard key={m.id} memory={m} />
          ))}
        </div>
      </div>
    </div>
  )
}
