import { useState, useEffect } from 'react'
import { Film, Boxes, Zap, Clock } from 'lucide-react'

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-bg-card border border-border-subtle rounded-xl p-5 hover:border-orbital-violet/30 transition-colors">
      <div className="flex items-center gap-3 mb-3">
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center`}
          style={{ background: `${color}15` }}>
          <Icon size={18} style={{ color }} />
        </div>
        <span className="text-sm text-text-muted">{label}</span>
      </div>
      <p className="text-2xl font-bold" style={{ color }}>{value}</p>
    </div>
  )
}

function VideoTypeCard({ id, data }) {
  const colors = {
    short: '#22D3EE',
    lesson: '#8B5CF6',
    problem: '#D6BC82',
    longform: '#39FF14',
  }
  const color = colors[id] || '#888'
  const layout = data.layout === 'short' ? '9:16' : '16:9'
  const dur = data.duration_range
  const durText = `${Math.floor(dur[0]/60)}-${Math.floor(dur[1]/60)} min`

  return (
    <div className="bg-bg-card border border-border-subtle rounded-xl p-5 hover:border-orbital-violet/30 transition-all group cursor-pointer">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-bold text-base" style={{ color }}>{data.label}</h3>
        <span className="text-xs text-text-muted px-2 py-0.5 rounded bg-bg-dark">{layout}</span>
      </div>
      <div className="space-y-2 text-sm text-text-muted">
        <div className="flex justify-between">
          <span>Duration</span>
          <span>{durText}</span>
        </div>
        <div className="flex justify-between">
          <span>TTS Profile</span>
          <span className="capitalize">{data.tts_profile}</span>
        </div>
        {data.sub_types && (
          <div className="flex justify-between">
            <span>Sub-types</span>
            <span>{data.sub_types.join(', ')}</span>
          </div>
        )}
      </div>
    </div>
  )
}

function TTSProfileCard({ id, profile }) {
  return (
    <div className="bg-bg-card border border-border-subtle rounded-xl p-4">
      <h4 className="font-semibold text-sm text-orbital-cyan capitalize mb-2">{id}</h4>
      <p className="text-xs text-text-muted mb-3">{profile.description}</p>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="flex justify-between">
          <span className="text-text-muted">Speed</span>
          <span>{profile.speed}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-text-muted">Stability</span>
          <span>{profile.stability}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-text-muted">Similarity</span>
          <span>{profile.similarity_boost}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-text-muted">Style</span>
          <span>{profile.style}</span>
        </div>
      </div>
    </div>
  )
}

export default function Dashboard({ config }) {
  const [libraryStats, setLibraryStats] = useState(null)
  const [outputs, setOutputs] = useState([])

  useEffect(() => {
    fetch('/api/library/stats').then(r => r.json()).then(setLibraryStats).catch(() => {})
    fetch('/api/outputs').then(r => r.json()).then(d => setOutputs(d.files || [])).catch(() => {})
  }, [])

  if (!config) return <div className="text-text-muted">Loading...</div>

  return (
    <div className="max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-orbital-cyan tracking-wide">ORBITAL ENGINE</h1>
        <p className="text-text-muted mt-1">Unified video production platform</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <StatCard icon={Boxes} label="Visual Components"
          value={libraryStats?.total_components ?? '—'} color="#8B5CF6" />
        <StatCard icon={Film} label="Video Types"
          value={Object.keys(config.video_types).length} color="#22D3EE" />
        <StatCard icon={Zap} label="TTS Profiles"
          value={Object.keys(config.tts_profiles).length} color="#D6BC82" />
        <StatCard icon={Clock} label="Rendered Videos"
          value={outputs.length} color="#39FF14" />
      </div>

      {/* Video Types */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-text-primary mb-4">Video Types</h2>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(config.video_types).map(([id, data]) => (
            <VideoTypeCard key={id} id={id} data={data} />
          ))}
        </div>
      </div>

      {/* TTS Profiles */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-text-primary mb-4">TTS Profiles — Allison</h2>
        <div className="grid grid-cols-4 gap-4">
          {Object.entries(config.tts_profiles).map(([id, profile]) => (
            <TTSProfileCard key={id} id={id} profile={profile} />
          ))}
        </div>
      </div>

      {/* Visual Library by Topic */}
      {libraryStats && (
        <div>
          <h2 className="text-lg font-semibold text-text-primary mb-4">Visual Library Coverage</h2>
          <div className="grid grid-cols-3 gap-3">
            {Object.entries(libraryStats.by_topic).map(([topic, count]) => (
              <div key={topic} className="bg-bg-card border border-border-subtle rounded-lg p-3 flex justify-between items-center">
                <span className="text-sm capitalize">{topic}</span>
                <span className={`text-sm font-mono ${count > 0 ? 'text-orbital-green' : 'text-text-muted'}`}>
                  {count} {count === 1 ? 'component' : 'components'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
