'use client'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { SessionTimeline } from '@/components/SessionTimeline'

export default function SessionsPage() {
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['sessions'],
    queryFn: () => api.get('/api/v1/sessions?limit=50'),
  })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Session Timeline</h1>
      {isLoading && <p className="text-gray-400 animate-pulse">Loading sessions...</p>}
      <SessionTimeline sessions={sessions} />
    </div>
  )
}
