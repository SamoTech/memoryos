'use client';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Clock, MessageSquare } from 'lucide-react';

export default function SessionsPage() {
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['sessions'],
    queryFn: api.sessions.list,
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Sessions</h1>
      {isLoading ? <p className="text-gray-500">Loading...</p> : (
        <div className="space-y-3">
          {sessions.map((s: any) => (
            <div key={s.id} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-indigo-600/20 flex items-center justify-center shrink-0">
                <Clock size={16} className="text-indigo-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-gray-200 truncate">{s.title || 'Untitled session'}</div>
                <div className="text-xs text-gray-500 mt-0.5">
                  {s.source} · {new Date(s.started_at).toLocaleString()}
                </div>
                {s.summary && <p className="text-xs text-gray-400 mt-1 line-clamp-2">{s.summary}</p>}
              </div>
              <div className="flex items-center gap-1 text-xs text-gray-500 shrink-0">
                <MessageSquare size={12} />
                {s.memory_count}
              </div>
            </div>
          ))}
          {sessions.length === 0 && <p className="text-gray-500">No sessions yet.</p>}
        </div>
      )}
    </div>
  );
}
