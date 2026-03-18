import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Library from './pages/Library'
import NewRender from './pages/NewRender'
import Outputs from './pages/Outputs'

export default function App() {
  const [page, setPage] = useState('dashboard')
  const [config, setConfig] = useState(null)

  useEffect(() => {
    fetch('/api/config').then(r => r.json()).then(setConfig).catch(console.error)
  }, [])

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar page={page} setPage={setPage} />
      <main className="flex-1 overflow-y-auto p-8">
        {page === 'dashboard' && <Dashboard config={config} />}
        {page === 'library' && <Library />}
        {page === 'render' && <NewRender config={config} />}
        {page === 'outputs' && <Outputs />}
      </main>
    </div>
  )
}
