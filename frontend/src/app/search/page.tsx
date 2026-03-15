'use client'
import { useState } from 'react'
import { useSearch } from '@/hooks/useSearch'
import { SearchBar } from '@/components/SearchBar'
import { MemoryCard } from '@/components/MemoryCard'
import { motion, AnimatePresence } from 'framer-motion'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const { results, isLoading } = useSearch(query)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Semantic Search</h1>
      <SearchBar value={query} onChange={setQuery} autoFocus />
      {isLoading && <p className="text-gray-400 animate-pulse">Searching your memories...</p>}
      <AnimatePresence>
        {results.map((item: any, i: number) => (
          <motion.div
            key={item.memory.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ delay: i * 0.04 }}
          >
            <MemoryCard memory={item.memory} score={item.score} />
          </motion.div>
        ))}
      </AnimatePresence>
      {!isLoading && query && results.length === 0 && (
        <p className="text-gray-500">No memories found for &ldquo;{query}&rdquo;</p>
      )}
    </div>
  )
}
