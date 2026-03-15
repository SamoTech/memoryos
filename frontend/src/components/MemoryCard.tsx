'use client';
import { motion } from 'framer-motion';
import { Pin, Trash2, Tag } from 'lucide-react';
import clsx from 'clsx';
import { usePinMemory, useForgetMemory } from '@/hooks/useMemories';

const SOURCE_COLORS: Record<string, string> = {
  chatgpt: 'bg-green-500/10 text-green-400',
  claude:  'bg-orange-500/10 text-orange-400',
  gemini:  'bg-blue-500/10 text-blue-400',
  cursor:  'bg-purple-500/10 text-purple-400',
  manual:  'bg-gray-500/10 text-gray-400',
  api:     'bg-cyan-500/10 text-cyan-400',
  cli:     'bg-yellow-500/10 text-yellow-400',
};

export default function MemoryCard({ memory }: { memory: any }) {
  const pin = usePinMemory();
  const forget = useForgetMemory();
  const text = memory.summary || memory.content;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={clsx(
        'bg-gray-900 border rounded-xl p-4 flex flex-col gap-3',
        memory.is_pinned ? 'border-indigo-500/50' : 'border-gray-800',
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <span className={clsx('text-xs font-semibold px-2 py-0.5 rounded-full uppercase', SOURCE_COLORS[memory.source] || SOURCE_COLORS.manual)}>
          {memory.source}
        </span>
        <div className="flex gap-1">
          <button
            onClick={() => pin.mutate(memory.id)}
            className={clsx('p-1 rounded hover:bg-gray-800 transition', memory.is_pinned ? 'text-indigo-400' : 'text-gray-600')}
            title={memory.is_pinned ? 'Unpin' : 'Pin'}
          >
            <Pin size={13} />
          </button>
          <button
            onClick={() => { if (confirm('Forget this memory?')) forget.mutate(memory.id); }}
            className="p-1 rounded hover:bg-red-900/30 text-gray-600 hover:text-red-400 transition"
            title="Forget"
          >
            <Trash2 size={13} />
          </button>
        </div>
      </div>

      <p className="text-sm text-gray-300 leading-relaxed line-clamp-4">{text}</p>

      <div className="flex items-center justify-between mt-auto">
        {memory.tags?.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {memory.tags.map((t: any) => (
              <span key={t.id} className="text-xs px-1.5 py-0.5 rounded" style={{ background: `${t.color}22`, color: t.color }}>
                {t.name}
              </span>
            ))}
          </div>
        )}
        <span className="text-xs text-gray-600 ml-auto">{new Date(memory.created_at).toLocaleDateString()}</span>
      </div>

      <div className="w-full bg-gray-800 rounded-full h-1">
        <div
          className="bg-indigo-500 h-1 rounded-full"
          style={{ width: `${(memory.importance_score || 0) * 100}%` }}
        />
      </div>
    </motion.div>
  );
}
