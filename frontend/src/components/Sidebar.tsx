'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Brain, Search, Clock, Tag, Settings, Download, BarChart2 } from 'lucide-react';
import clsx from 'clsx';

const NAV = [
  { href: '/', label: 'Dashboard', icon: BarChart2 },
  { href: '/memories', label: 'Memories', icon: Brain },
  { href: '/search', label: 'Search', icon: Search },
  { href: '/sessions', label: 'Sessions', icon: Clock },
  { href: '/export', label: 'Export', icon: Download },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside className="w-56 bg-gray-900 border-r border-gray-800 flex flex-col py-6 px-3 shrink-0">
      <div className="flex items-center gap-2 px-3 mb-8">
        <span className="text-2xl">🧠</span>
        <span className="font-bold text-indigo-400 text-lg">MemoryOS</span>
      </div>
      <nav className="flex flex-col gap-1">
        {NAV.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
              path === href
                ? 'bg-indigo-600/20 text-indigo-400'
                : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100',
            )}
          >
            <Icon size={16} />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
