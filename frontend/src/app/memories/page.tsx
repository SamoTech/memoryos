'use client';
import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import MemoryCard from '@/components/MemoryCard';
import SearchBar from '@/components/SearchBar';
import { useMemories } from '@/hooks/useMemories';

const SOURCES = ['all', 'chatgpt', 'claude', 'gemini', 'cursor', 'manual', 'cli', 'api'];

export default function MemoriesPage() {
  const [source, setSource] = useState('all');
  const [pinned, setPinned] = useState(false);
  const [search, setSearch] = useState('');

  const { data: memories = [], isLoading } = useMemories({
    limit: 100,
    ...(source !== 'all' && { source }),
    ...(pinned && { pinned: 'true' }),
  });

  const filtered = memories.filter((m: any) =>
    !search || m.content.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Memories</h1>
        <span className="text-sm text-gray-500">{filtered.length} total</span>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <SearchBar value={search} onChange={setSearch} />
        <div className="flex gap-2 flex-wrap">
          {SOURCES.map((s) => (
            <button
              key={s}
              onClick={() => setSource(s)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
                source === s ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
        <button
          onClick={() => setPinned(!pinned)}
          className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
            pinned ? 'bg-purple-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          }`}
        >
          📌 Pinned only
        </button>
      </div>

      {isLoading ? (
        <div className="text-gray-500">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <AnimatePresence mode="popLayout">
            {filtered.map((m: any) => <MemoryCard key={m.id} memory={m} />)}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
