const SOURCE_CONFIG: Record<string, { label: string; color: string; emoji: string }> = {
  chatgpt: { label: 'ChatGPT', color: '#10a37f', emoji: '🧠' },
  claude:  { label: 'Claude',  color: '#d97757', emoji: '🌐' },
  gemini:  { label: 'Gemini',  color: '#4285f4', emoji: '✨' },
  cursor:  { label: 'Cursor',  color: '#a78bfa', emoji: '💻' },
  manual:  { label: 'Manual',  color: '#6b7280', emoji: '✏️' },
  cli:     { label: 'CLI',     color: '#22d3ee', emoji: '🖥️' },
  api:     { label: 'API',     color: '#f59e0b', emoji: '🔗' },
}

export function SourceBadge({ source }: { source: string }) {
  const cfg = SOURCE_CONFIG[source] ?? { label: source, color: '#6b7280', emoji: '💾' }
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full font-medium"
      style={{ backgroundColor: cfg.color + '22', color: cfg.color, border: `1px solid ${cfg.color}44` }}
    >
      {cfg.emoji} {cfg.label}
    </span>
  )
}
