import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useMemories(params?: Record<string, any>) {
  return useQuery({
    queryKey: ['memories', params],
    queryFn: () => api.memories.list(params),
    refetchInterval: 15_000,
  });
}

export function useForgetMemory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.memories.forget(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['memories'] }),
  });
}

export function usePinMemory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.memories.pin(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['memories'] }),
  });
}

export function useAddMemory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: any) => api.memories.add(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['memories'] }),
  });
}

export function useStats() {
  return useQuery({ queryKey: ['stats'], queryFn: api.stats, refetchInterval: 30_000 });
}
