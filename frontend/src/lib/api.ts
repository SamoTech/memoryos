const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8765'

export const api = {
  get: async (path: string) => {
    const res = await fetch(`${BASE}${path}`)
    if (!res.ok) throw new Error(`API error ${res.status}`)
    return res.json()
  },
  post: async (path: string, body?: unknown) => {
    const res = await fetch(`${BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    })
    if (!res.ok) throw new Error(`API error ${res.status}`)
    return res.json()
  },
  delete: async (path: string) => {
    const res = await fetch(`${BASE}${path}`, { method: 'DELETE' })
    if (!res.ok) throw new Error(`API error ${res.status}`)
    return res.status === 204 ? null : res.json()
  },
}
