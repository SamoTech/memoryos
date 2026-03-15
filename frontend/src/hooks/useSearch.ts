import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useSearch(query: string, limit = 10) {
  const { data: results = [], isLoading } = useQuery({
    queryKey: ['search', query, limit],
    queryFn: () => api.get(`/api/v1/search?q=${encodeURIComponent(query)}&limit=${limit}`),
    enabled: query.length >= 2,
  })

  return { results, isLoading }
}
