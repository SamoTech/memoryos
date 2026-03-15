'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Brain, Search, BookOpen, Clock, Settings, Download } from 'lucide-react'

const NAV = [
  { href: '/',          label: 'Dashboard',  icon: Brain },
  { href: '/memories',  label: 'Memories',   icon: BookOpen },
  { href: '/search',    label: 'Search',     icon: Search },
  { href: '/sessions',  label: 'Sessions',   icon: Clock },
  { href: '/settings',  label: 'Settings',   icon: Settings },
  { href: '/export',    label: 'Export',     icon: Download },
]

export function Sidebar() {
  const pathname = usePathname()
  return (
    <aside className="w-56 shrink-0 bg-gray-950 border-r border-gray-800 flex flex-col py-6 px-3 gap-1">
      <div className="px-3 mb-6">
        <h1 className="text-lg font-bold text-white flex items-center gap-2">
          <Brain size={22} className="text-indigo-400" /> MemoryOS
        </h1>
        <p className="text-xs text-gray-500 mt-0.5">v1.0.0</p>
      </div>
      {NAV.map(({ href, label, icon: Icon }) => {
        const active = pathname === href
        return (
          <Link
            key={href}
            href={href}
            className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors ${
              active
                ? 'bg-indigo-500/20 text-indigo-300 font-medium'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
            }`}
          >
            <Icon size={16} />
            {label}
          </Link>
        )
      })}
    </aside>
  )
}
