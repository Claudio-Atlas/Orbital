import { useState, useEffect } from 'react'
import { FileVideo, Download, Trash2 } from 'lucide-react'

export default function Outputs() {
  const [files, setFiles] = useState([])

  useEffect(() => {
    fetch('/api/outputs').then(r => r.json())
      .then(d => setFiles(d.files || []))
      .catch(console.error)
  }, [])

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-orbital-green tracking-wide">Outputs</h1>
        <p className="text-text-muted mt-1">Rendered videos ready for upload</p>
      </div>

      {files.length === 0 ? (
        <div className="bg-bg-card border border-border-subtle rounded-xl p-12 text-center">
          <FileVideo size={48} className="text-text-muted mx-auto mb-4 opacity-30" />
          <p className="text-text-muted">No rendered videos yet</p>
          <p className="text-xs text-text-muted mt-1">Start a render to see outputs here</p>
        </div>
      ) : (
        <div className="space-y-3">
          {files.map(file => (
            <div key={file.name}
              className="bg-bg-card border border-border-subtle rounded-xl p-4 flex items-center justify-between hover:border-orbital-violet/30 transition-colors">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-lg bg-orbital-green/10 flex items-center justify-center">
                  <FileVideo size={18} className="text-orbital-green" />
                </div>
                <div>
                  <p className="text-sm font-semibold">{file.name}</p>
                  <p className="text-xs text-text-muted">
                    {file.size_mb} MB · {new Date(file.modified * 1000).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
