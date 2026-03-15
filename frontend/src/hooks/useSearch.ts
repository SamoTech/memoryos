import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useSearch() {
  const [query, setQuery] = useState('');
  const [debouncedQ, setDebouncedQ] = useState('');

  const search = useCallback((q: string) => {
    setQuery(q);
    const t = setTimeout(() => setDebouncedQ(q), 300);
    return () => clearTimeout(t);
  }, []);

  const results = useQuery({
    queryKey: ['search', debouncedQ],
    queryFn: () => api.search.hybrid(debouncedQ, 20),
    enabled: debouncedQ.length >= 2,
  });

  return { query, search, results };
}
