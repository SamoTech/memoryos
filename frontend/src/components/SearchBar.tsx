'use client';
import { Search, X } from 'lucide-react';

export default function SearchBar({
  value, onChange, placeholder = 'Search memories...'
}: { value: string; onChange: (v: string) => void; placeholder?: string }) {
  return (
    <div className="relative w-full">
      <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-gray-900 border border-gray-800 rounded-xl pl-9 pr-9 py-2.5 text-sm text-gray-100 placeholder-gray-500 outline-none focus:border-indigo-500 transition"
      />
      {value && (
        <button onClick={() => onChange('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
          <X size={14} />
        </button>
      )}
    </div>
  );
}
