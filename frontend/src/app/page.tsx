'use client';
import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import StatsWidget from '@/components/StatsWidget';
import MemoryCard from '@/components/MemoryCard';
import SearchBar from '@/components/SearchBar';
import { useMemories } from '@/hooks/useMemories';
import { useSearch } from '@/hooks/useSearch';

export default function Dashboard() {
  const { query, search, results: searchResults } = useSearch();
  const { data: recent } = useMemories({ limit: 20 });

  const displayItems = query.length >= 2
    ? (searchResults.data || [])
    : (recent || []).map((m: any) => ({ memory: m, score: 1 }));

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-100">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">Your AI finally remembers you.</p>
      </div>

      <StatsWidget />

      <SearchBar value={query} onChange={search} placeholder="Search all memories semantically..." />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <AnimatePresence mode="popLayout">
          {displayItems.map((item: any) => (
            <MemoryCard key={item.memory?.id || item.id} memory={item.memory || item} />
          ))}
        </AnimatePresence>
      </div>

      {displayItems.length === 0 && (
        <div className="text-center py-24 text-gray-600">
          <div className="text-5xl mb-4">🧠</div>
          <p className="text-lg">No memories yet.</p>
          <p className="text-sm mt-1">Install the browser extension and start chatting with any AI.</p>
        </div>
      )}
    </div>
  );
}
