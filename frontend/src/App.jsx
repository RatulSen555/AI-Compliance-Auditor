import { useState } from 'react'
import Upload from './components/Upload'
import Interview from './components/Interview'
import Dashboard from './components/Dashboard'

export default function App() {
  const [tab, setTab] = useState('analyze')
  const [report, setReport] = useState(null)

  const tabs = [
    { id: 'analyze', label: 'Analyze Room', icon: '🔍' },
    { id: 'interview', label: 'Voice Interview', icon: '🎤' },
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  ]

  return (
    <div className="min-h-screen">
      <div className="bg-slate-800/80 border-b border-slate-700 px-6 py-4 flex items-center justify-between sticky top-0 z-50 backdrop-blur">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🛡️</span>
          <h1 className="text-xl font-bold text-white">Compliance Auditor</h1>
        </div>
        <div className="flex gap-1 bg-slate-900/50 p-1 rounded-lg">
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all cursor-pointer ${tab === t.id ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}>
              <span className="mr-1">{t.icon}</span> {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {tab === 'analyze' && <Upload onReport={setReport} report={report} />}
        {tab === 'interview' && <Interview />}
        {tab === 'dashboard' && <Dashboard />}
      </div>
    </div>
  )
}