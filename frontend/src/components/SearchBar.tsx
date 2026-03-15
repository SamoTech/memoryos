'use client'
import { Search } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export function SearchBar({
  value,
  onChange,
  autoFocus = false,
}: {
  value?: string
  onChange?: (v: string) => void
  autoFocus?: boolean
}) {
  const router = useRouter()
  const [local, setLocal] = useState('')
  const controlled = value !== undefined
  const current = controlled ? value : local

  const handleChange = (v: string) => {
    if (controlled) onChange?.(v)
    else setLocal(v)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !controlled) {
      router.push(`/search?q=${encodeURIComponent(current)}`)
    }
  }

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
      <input
        autoFocus={autoFocus}
        type="text"
        placeholder="Search your memories..."
        value={current}
        onChange={e => handleChange(e.target.value)}
        onKeyDown={handleKeyDown}
        className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-indigo-500 transition-colors"
      />
    </div>
  )
}
