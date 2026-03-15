import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

interface UseMemoriesOptions {
  source?: string
  pinnedOnly?: boolean
  limit?: number
}

export function useMemories({ source, pinnedOnly, limit = 50 }: UseMemoriesOptions = {}) {
  const params = new URLSearchParams({ limit: String(limit) })
  if (source) params.set('source', source)
  if (pinnedOnly) params.set('pinned_only', 'true')

  const { data: memories = [], isLoading, error } = useQuery({
    queryKey: ['memories', source, pinnedOnly, limit],
    queryFn: () => api.get(`/api/v1/memories?${params}`),
  })

  return { memories, isLoading, error }
}
