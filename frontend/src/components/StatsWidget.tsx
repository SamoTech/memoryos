import { ReactNode } from 'react'

const colorMap: Record<string, string> = {
  indigo: 'text-indigo-400 bg-indigo-400/10 border-indigo-500/20',
  violet: 'text-violet-400 bg-violet-400/10 border-violet-500/20',
  emerald: 'text-emerald-400 bg-emerald-400/10 border-emerald-500/20',
  amber: 'text-amber-400 bg-amber-400/10 border-amber-500/20',
}

export function StatsWidget({ label, value, icon, color = 'indigo' }: {
  label: string; value: string | number; icon: ReactNode; color?: string
}) {
  const cls = colorMap[color] || colorMap.indigo
  return (
    <div className={`rounded-xl border p-4 flex items-center gap-3 ${cls}`}>
      <div className="text-xl">{icon}</div>
      <div>
        <p className="text-2xl font-bold text-white">{value}</p>
        <p className="text-xs text-gray-400">{label}</p>
      </div>
    </div>
  )
}
