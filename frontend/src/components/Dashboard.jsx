import React, { useState, useEffect } from 'react'
import { getHistory } from '../api'

export default function Dashboard() {
  const [history, setHistory] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadHistory = async () => {
    setLoading(true)
    try {
      const data = await getHistory()
      setHistory(data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  useEffect(() => { loadHistory() }, [])

  const getScoreColor = (s) => s >= 80 ? 'text-green-400' : s >= 50 ? 'text-yellow-400' : 'text-red-400'
  const getBarColor = (s) => s >= 80 ? 'bg-green-500' : s >= 50 ? 'bg-yellow-500' : 'bg-red-500'

  if (loading) return <div className="text-center py-16 text-slate-400 text-lg">Loading history...</div>
  if (!history) return <div className="text-center py-16 text-red-400">Failed to load</div>

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">📊 Score History</h2>
        <button onClick={loadHistory} className="text-sm text-slate-400 hover:text-white transition-colors">🔄 Refresh</button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
          <p className="text-3xl font-bold text-white">{history.checks.length}</p>
          <p className="text-sm text-slate-400">Room Analyses</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
          <p className="text-3xl font-bold text-white">{history.interviews.length}</p>
          <p className="text-sm text-slate-400">Interviews</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
          <p className="text-3xl font-bold text-white">{history.checks.length ? Math.round(history.checks.reduce((a, c) => a + c.score, 0) / history.checks.length) : 0}</p>
          <p className="text-sm text-slate-400">Avg Score</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
          <p className="text-3xl font-bold text-white">{history.interviews.length ? Math.round(history.interviews.reduce((a, c) => a + c.total_score, 0) / history.interviews.length) : 0}</p>
          <p className="text-sm text-slate-400">Avg Interview</p>
        </div>
      </div>

      {/* Room Analyses */}
      <div>
        <h3 className="text-lg font-semibold text-slate-300 mb-4">🔍 Room Analyses</h3>
        {history.checks.length === 0 ? (
          <p className="text-slate-500 bg-slate-800/50 rounded-xl p-6 text-center">No analyses yet. Go to Analyze Room tab to upload a photo.</p>
        ) : (
          <div className="space-y-3">
            {history.checks.map((c, i) => {
              const gaps = JSON.parse(c.gaps || '[]')
              return (
                <div key={i} className="bg-slate-800 rounded-xl p-4 border border-slate-700">
                  <div className="flex items-center gap-4">
                    <div className="text-center min-w-[70px]">
                      <p className={`text-2xl font-bold ${getScoreColor(c.score)}`}>{c.score}</p>
                      <p className="text-xs text-slate-500">/100</p>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white font-medium">{c.standard}</span>
                        <span className="text-slate-500 text-sm">{new Date(c.created_at).toLocaleDateString()}</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2 mb-2">
                        <div className={`${getBarColor(c.score)} h-2 rounded-full transition-all`} style={{ width: `${c.score}%` }} />
                      </div>
                      <p className="text-sm text-slate-400 truncate">{c.summary}</p>
                      <div className="flex gap-1 mt-2 flex-wrap">
                        {gaps.slice(0, 3).map((g, j) => (
                          <span key={j} className={`text-xs px-2 py-0.5 rounded ${g.severity === 'high' ? 'bg-red-500/20 text-red-400' : g.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-blue-500/20 text-blue-400'}`}>{g.area}</span>
                        ))}
                        {gaps.length > 3 && <span className="text-xs text-slate-500">+{gaps.length - 3} more</span>}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Interviews */}
      <div>
        <h3 className="text-lg font-semibold text-slate-300 mb-4">🎤 Interview Sessions</h3>
        {history.interviews.length === 0 ? (
          <p className="text-slate-500 bg-slate-800/50 rounded-xl p-6 text-center">No interviews yet. Go to Voice Interview tab to start.</p>
        ) : (
          <div className="space-y-3">
            {history.interviews.map((s, i) => {
              const answers = JSON.parse(s.answers || '[]')
              return (
                <div key={i} className="bg-slate-800 rounded-xl p-4 border border-slate-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-medium">{s.standard}</span>
                    <span className={`text-xl font-bold ${getScoreColor(s.total_score)}`}>{s.total_score}/100</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2 mb-3">
                    <div className={`${getBarColor(s.total_score)} h-2 rounded-full`} style={{ width: `${s.total_score}%` }} />
                  </div>
                  {answers.length > 0 && (
                    <div className="flex gap-2 flex-wrap mb-2">
                      {answers.map((a, j) => (
                        <div key={j} className="text-xs bg-slate-700 rounded-lg px-3 py-1.5">
                          <span className="text-slate-400">Q{j + 1}: </span>
                          <span className={`font-bold ${a.score >= 15 ? 'text-green-400' : a.score >= 10 ? 'text-yellow-400' : 'text-red-400'}`}>{a.score}</span>
                          <span className="text-slate-500">/20</span>
                        </div>
                      ))}
                    </div>
                  )}
                  <p className="text-xs text-slate-500">{new Date(s.created_at).toLocaleString()} · {answers.length} questions answered</p>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}