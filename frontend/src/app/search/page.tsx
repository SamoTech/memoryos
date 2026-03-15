'use client';
import { useState } from 'react';
import { useSearch } from '@/hooks/useSearch';
import SearchBar from '@/components/SearchBar';
import MemoryCard from '@/components/MemoryCard';

export default function SearchPage() {
  const { query, search, results } = useSearch();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Semantic Search</h1>
      <SearchBar
        value={query}
        onChange={search}
        placeholder="Ask your memories anything..."
      />
      {results.isFetching && <p className="text-gray-500 text-sm">Searching...</p>}
      {results.data && results.data.length > 0 && (
        <div className="space-y-4">
          {results.data.map((item: any) => (
            <div key={item.memory.id} className="space-y-1">
              <div className="text-xs text-gray-500">Score: {(item.score * 100).toFixed(0)}%</div>
              <MemoryCard memory={item.memory} />
            </div>
          ))}
        </div>
      )}
      {results.data?.length === 0 && query.length >= 2 && (
        <p className="text-gray-500">No results for "{query}"</p>
      )}
    </div>
  );
}
