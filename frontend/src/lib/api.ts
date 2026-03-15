const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8765';

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const resp = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  });
  if (!resp.ok) throw new Error(`API error ${resp.status}: ${await resp.text()}`);
  return resp.json();
}

export const api = {
  memories: {
    list: (params?: Record<string, string | number>) => {
      const q = params ? '?' + new URLSearchParams(params as any).toString() : '';
      return apiFetch<any[]>(`/api/v1/memories${q}`);
    },
    get: (id: string) => apiFetch<any>(`/api/v1/memories/${id}`),
    add: (body: any) => apiFetch<any>('/api/v1/memories', { method: 'POST', body: JSON.stringify(body) }),
    forget: (id: string) => apiFetch<any>(`/api/v1/memories/${id}`, { method: 'DELETE' }),
    pin: (id: string) => apiFetch<any>(`/api/v1/memories/${id}/pin`, { method: 'POST' }),
  },
  search: {
    hybrid: (q: string, limit = 10) => apiFetch<any[]>(`/api/v1/search?q=${encodeURIComponent(q)}&limit=${limit}`),
    context: (q: string) => apiFetch<any>(`/api/v1/search/context?q=${encodeURIComponent(q)}`),
  },
  sessions: {
    list: () => apiFetch<any[]>('/api/v1/sessions'),
    get: (id: string) => apiFetch<any>(`/api/v1/sessions/${id}`),
  },
  stats: () => apiFetch<any>('/api/v1/stats'),
  tags: () => apiFetch<any[]>('/api/v1/tags'),
  health: () => apiFetch<any>('/health'),
};
