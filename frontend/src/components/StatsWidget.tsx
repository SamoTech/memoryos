'use client';
import { Brain, Pin, HardDrive, Zap } from 'lucide-react';
import { useStats } from '@/hooks/useMemories';

export default function StatsWidget() {
  const { data: stats, isLoading } = useStats();
  if (isLoading) return <div className="text-gray-500 text-sm">Loading stats...</div>;
  if (!stats) return null;

  const items = [
    { icon: Brain, label: 'Memories', value: stats.total_memories, color: 'text-indigo-400' },
    { icon: Pin, label: 'Pinned', value: stats.pinned_memories, color: 'text-purple-400' },
    { icon: HardDrive, label: 'Storage', value: `${stats.storage_mb} MB`, color: 'text-cyan-400' },
    { icon: Zap, label: 'Sources', value: Object.keys(stats.by_source || {}).length, color: 'text-green-400' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {items.map(({ icon: Icon, label, value, color }) => (
        <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex flex-col gap-2">
          <Icon size={18} className={color} />
          <div className="text-2xl font-bold text-gray-100">{value}</div>
          <div className="text-xs text-gray-500">{label}</div>
        </div>
      ))}
    </div>
  );
}
