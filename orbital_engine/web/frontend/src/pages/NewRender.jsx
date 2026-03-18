import { useState, useEffect } from 'react'
import { Film, Play, BookOpen } from 'lucide-react'

export default function NewRender({ config }) {
  const [videoType, setVideoType] = useState('')
  const [topic, setTopic] = useState('')
  const [chapter, setChapter] = useState('')
  const [section, setSection] = useState('')
  const [videoSub, setVideoSub] = useState('A')
  const [sections, setSections] = useState([])
  const [rendering, setRendering] = useState(false)
  const [result, setResult] = useState(null)

  useEffect(() => {
    fetch('/api/textbook/sections').then(r => r.json())
      .then(d => setSections(d.sections || []))
      .catch(() => {})
  }, [])

  if (!config) return <div className="text-text-muted">Loading...</div>

  const selectedType = config.video_types[videoType]
  const hasSubs = selectedType?.sub_types

  const handleRender = async () => {
    setRendering(true)
    setResult(null)
    try {
      const res = await fetch('/api/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_type: videoType,
          topic,
          chapter: chapter ? parseInt(chapter) : null,
          section: section ? parseInt(section) : null,
          video_sub: hasSubs ? videoSub : null,
        }),
      })
      const data = await res.json()

      if (data.job_id) {
        // Poll for progress
        const poll = async () => {
          try {
            const pr = await fetch(`/api/renders/${data.job_id}/poll`)
            const status = await pr.json()
            setResult(status)
            if (status.status !== 'complete' && status.status !== 'error') {
              setTimeout(poll, 2000)
            } else {
              setRendering(false)
            }
          } catch {
            setRendering(false)
          }
        }
        setResult({ status: 'queued', progress: 0, id: data.job_id })
        poll()
      } else {
        setResult(data)
        setRendering(false)
      }
    } catch (e) {
      setResult({ error: e.message })
      setRendering(false)
    }
  }

  // Group sections by chapter
  const sectionsByChapter = sections.reduce((acc, s) => {
    if (!acc[s.chapter]) acc[s.chapter] = []
    acc[s.chapter].push(s)
    return acc
  }, {})

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-orbital-gold tracking-wide">New Render</h1>
        <p className="text-text-muted mt-1">Configure and produce a video</p>
      </div>

      <div className="space-y-6">
        {/* Video Type Selection */}
        <div>
          <label className="block text-sm font-medium text-text-muted mb-3">Video Type</label>
          <div className="grid grid-cols-4 gap-3">
            {Object.entries(config.video_types).map(([id, data]) => {
              const colors = { short: '#22D3EE', lesson: '#8B5CF6', problem: '#D6BC82', longform: '#39FF14' }
              const color = colors[id] || '#888'
              const active = videoType === id
              return (
                <button key={id} onClick={() => setVideoType(id)}
                  className={`p-4 rounded-xl border text-left transition-all
                    ${active
                      ? 'border-orbital-violet/50 bg-orbital-violet/10'
                      : 'border-border-subtle bg-bg-card hover:bg-bg-card-hover'}`}
                >
                  <Film size={20} style={{ color }} className="mb-2" />
                  <p className="text-sm font-semibold" style={{ color }}>{data.label}</p>
                  <p className="text-xs text-text-muted mt-1">
                    {data.layout === 'short' ? '9:16' : '16:9'}
                  </p>
                </button>
              )
            })}
          </div>
        </div>

        {/* Section Selection (for lesson/problem types) */}
        {(videoType === 'lesson' || videoType === 'problem') && (
          <div>
            <label className="block text-sm font-medium text-text-muted mb-3">
              <BookOpen size={14} className="inline mr-1" /> Textbook Section
            </label>
            <div className="bg-bg-card border border-border-subtle rounded-xl p-4 max-h-64 overflow-y-auto space-y-3">
              {Object.entries(sectionsByChapter).map(([ch, secs]) => (
                <div key={ch}>
                  <p className="text-xs text-orbital-violet font-bold mb-1">Chapter {ch}</p>
                  <div className="space-y-1">
                    {secs.map(s => {
                      const active = chapter == s.chapter && section == s.section
                      return (
                        <button key={`${s.chapter}-${s.section}`}
                          onClick={() => { setChapter(s.chapter); setSection(s.section) }}
                          className={`w-full text-left px-3 py-1.5 rounded text-sm transition-colors
                            ${active
                              ? 'bg-orbital-violet/15 text-orbital-cyan'
                              : 'text-text-muted hover:text-text-primary hover:bg-bg-dark'}`}
                        >
                          §{s.chapter}.{s.section} — {s.title}
                          <span className="text-xs text-text-muted ml-2">
                            ({s.objectives} obj, {s.content_blocks} blocks)
                          </span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Video Sub-type (A/B/C for lessons) */}
        {hasSubs && (
          <div>
            <label className="block text-sm font-medium text-text-muted mb-3">Video Sub-type</label>
            <div className="flex gap-3">
              {selectedType.sub_types.map(sub => {
                const labels = { A: 'Concepts', B: 'Skills', C: 'Extensions' }
                return (
                  <button key={sub} onClick={() => setVideoSub(sub)}
                    className={`flex-1 py-3 rounded-xl border text-center transition-all
                      ${videoSub === sub
                        ? 'border-orbital-cyan/50 bg-orbital-cyan/10 text-orbital-cyan'
                        : 'border-border-subtle bg-bg-card text-text-muted hover:bg-bg-card-hover'}`}
                  >
                    <p className="text-lg font-bold">{sub}</p>
                    <p className="text-xs mt-0.5">{labels[sub] || sub}</p>
                  </button>
                )
              })}
            </div>
          </div>
        )}

        {/* TTS Profile Preview */}
        {videoType && config.tts_profiles[selectedType?.tts_profile] && (
          <div className="bg-bg-card border border-border-subtle rounded-xl p-4">
            <p className="text-xs text-text-muted mb-2">TTS Profile</p>
            <p className="text-sm text-orbital-cyan font-semibold capitalize mb-1">
              {selectedType.tts_profile}
            </p>
            <p className="text-xs text-text-muted">
              {config.tts_profiles[selectedType.tts_profile].description}
            </p>
          </div>
        )}

        {/* Render Button */}
        <button
          onClick={handleRender}
          disabled={!videoType || rendering}
          className={`w-full py-4 rounded-xl font-bold text-base flex items-center justify-center gap-2 transition-all
            ${!videoType || rendering
              ? 'bg-border-subtle text-text-muted cursor-not-allowed'
              : 'bg-orbital-violet hover:bg-orbital-violet/80 text-white glow-violet'}`}
        >
          <Play size={18} />
          {rendering ? 'Rendering...' : 'Start Render'}
        </button>

        {/* Result */}
        {result && (
          <div className={`p-5 rounded-xl border ${
            result.status === 'error' ? 'border-red-500/30 bg-red-500/5' :
            result.status === 'complete' ? 'border-orbital-green/30 bg-orbital-green/5' :
            'border-orbital-cyan/30 bg-orbital-cyan/5'
          }`}>
            {/* Progress */}
            {result.progress !== undefined && result.status !== 'complete' && result.status !== 'error' && (
              <div className="mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-orbital-cyan capitalize">{result.status?.replace('_', ' ')}</span>
                  <span className="text-text-muted">{result.progress}%</span>
                </div>
                <div className="h-2 bg-bg-dark rounded-full overflow-hidden">
                  <div className="h-full bg-orbital-cyan rounded-full transition-all duration-500"
                    style={{ width: `${result.progress}%` }} />
                </div>
              </div>
            )}

            {/* Complete */}
            {result.status === 'complete' && (
              <div className="space-y-2">
                <p className="text-orbital-green font-bold text-lg">✅ Render Complete</p>
                {result.duration && <p className="text-sm text-text-muted">Duration: {Math.round(result.duration)}s</p>}
                {result.size_mb && <p className="text-sm text-text-muted">Size: {result.size_mb} MB</p>}
                {result.desktop_path && <p className="text-sm text-text-muted">📋 Copied to Desktop</p>}
              </div>
            )}

            {/* Error */}
            {result.status === 'error' && (
              <div>
                <p className="text-red-400 font-bold mb-2">❌ Render Failed</p>
                <pre className="text-xs font-mono text-red-300 whitespace-pre-wrap">{result.error}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
