import { useState, useEffect } from 'react'
import { Boxes, Code, ChevronRight } from 'lucide-react'

const TOPIC_COLORS = {
  general: '#E0E0E0',
  functions: '#22D3EE',
  algebra: '#8B5CF6',
  polynomial: '#D6BC82',
  rational: '#F97316',
  exponential: '#39FF14',
  trigonometry: '#EC4899',
  calculus: '#00E5FF',
  graphs: '#8B5CF6',
}

export default function Library() {
  const [library, setLibrary] = useState(null)
  const [expanded, setExpanded] = useState(null)

  useEffect(() => {
    fetch('/api/library').then(r => r.json()).then(setLibrary).catch(console.error)
  }, [])

  if (!library) return <div className="text-text-muted">Loading visual library...</div>

  const totalComponents = Object.values(library).reduce((s, t) => s + t.count, 0)

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-orbital-violet tracking-wide">Visual Library</h1>
        <p className="text-text-muted mt-1">
          {totalComponents} components across {Object.keys(library).length} topics
        </p>
      </div>

      <div className="space-y-3">
        {Object.entries(library).map(([topic, data]) => {
          const color = TOPIC_COLORS[topic] || '#888'
          const isOpen = expanded === topic

          return (
            <div key={topic} className="bg-bg-card border border-border-subtle rounded-xl overflow-hidden">
              {/* Topic Header */}
              <button
                onClick={() => setExpanded(isOpen ? null : topic)}
                className="w-full flex items-center justify-between px-5 py-4 hover:bg-bg-card-hover transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center"
                    style={{ background: `${color}15` }}>
                    <Boxes size={16} style={{ color }} />
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold text-sm" style={{ color }}>
                      {data.label}
                    </h3>
                    <p className="text-xs text-text-muted">
                      {data.count} {data.count === 1 ? 'component' : 'components'}
                    </p>
                  </div>
                </div>
                <ChevronRight
                  size={18}
                  className={`text-text-muted transition-transform ${isOpen ? 'rotate-90' : ''}`}
                />
              </button>

              {/* Components List */}
              {isOpen && (
                <div className="border-t border-border-subtle px-5 py-3 space-y-2">
                  {data.components.length === 0 ? (
                    <p className="text-sm text-text-muted py-2 italic">
                      No components yet — needs building
                    </p>
                  ) : (
                    data.components.map(comp => (
                      <div key={comp.name}
                        className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-bg-dark transition-colors">
                        <Code size={14} style={{ color }} />
                        <div>
                          <span className="text-sm font-mono">{comp.name}</span>
                          {comp.description && (
                            <p className="text-xs text-text-muted mt-0.5">{comp.description}</p>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
