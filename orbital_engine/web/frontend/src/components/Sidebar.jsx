import { LayoutDashboard, Boxes, Film, FolderOutput } from 'lucide-react'

const NAV = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'library',   label: 'Visual Library', icon: Boxes },
  { id: 'render',    label: 'New Render', icon: Film },
  { id: 'outputs',   label: 'Outputs', icon: FolderOutput },
]

export default function Sidebar({ page, setPage }) {
  return (
    <aside className="w-64 bg-bg-card border-r border-border-subtle flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-border-subtle">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-orbital-violet/20 flex items-center justify-center">
            <span className="text-orbital-cyan text-lg font-bold">O</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-orbital-cyan tracking-wider">ORBITAL</h1>
            <p className="text-[10px] text-text-muted tracking-widest uppercase">Engine v1.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV.map(item => {
          const Icon = item.icon
          const active = page === item.id
          return (
            <button
              key={item.id}
              onClick={() => setPage(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all
                ${active
                  ? 'bg-orbital-violet/15 text-orbital-cyan border border-orbital-violet/30'
                  : 'text-text-muted hover:text-text-primary hover:bg-bg-card-hover border border-transparent'
                }`}
            >
              <Icon size={18} className={active ? 'text-orbital-cyan' : ''} />
              {item.label}
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-border-subtle">
        <p className="text-[11px] text-text-muted">
          Math, the way it should be.
        </p>
      </div>
    </aside>
  )
}
