import React, { useState, useRef } from 'react'
import { analyzeRoom } from '../api'

export default function Upload({ onReport, report }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [standard, setStandard] = useState('ISO 45001')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef()

  const handleFile = (e) => {
    const f = e.target.files[0]
    if (f) {
      setFile(f)
      setPreview(URL.createObjectURL(f))
      onReport(null)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f && f.type.startsWith('image/')) {
      setFile(f)
      setPreview(URL.createObjectURL(f))
      onReport(null)
    }
  }

  const analyze = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const result = await analyzeRoom(file, standard)
      onReport(result)
    } catch (err) {
      setError(err.message || 'Analysis failed')
    }
    setLoading(false)
  }

  const getScoreColor = (s) => s >= 80 ? 'text-green-400' : s >= 50 ? 'text-yellow-400' : 'text-red-400'
  const getSeverityColor = (s) => s === 'high' ? 'bg-red-500/20 text-red-400 border-red-500/30' : s === 'medium' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' : 'bg-blue-500/20 text-blue-400 border-blue-500/30'

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Upload */}
      <div className="space-y-4">
        <div
          onClick={() => inputRef.current.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          className="border-2 border-dashed border-slate-600 hover:border-blue-500 rounded-xl p-8 text-center cursor-pointer transition-all bg-slate-800/50 hover:bg-slate-800 min-h-[250px] flex items-center justify-center">
          {preview ? (
            <img src={preview} alt="Room" className="max-h-56 mx-auto rounded-lg" />
          ) : (
            <div className="space-y-2">
              <div className="text-4xl">📁</div>
              <p className="text-slate-400">Click or drag a room photo here</p>
              <p className="text-slate-500 text-sm">Supports JPG, PNG, WebP</p>
            </div>
          )}
          <input ref={inputRef} type="file" accept="image/*" onChange={handleFile} className="hidden" />
        </div>

        <div className="flex gap-3">
          <select value={standard} onChange={e => setStandard(e.target.value)}
            className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none">
            <option>ISO 45001</option>
            <option>OSHA</option>
            <option>NEBOSH</option>
            <option>NFPA 101</option>
            <option>Fire Safety</option>
          </select>
          <button onClick={analyze} disabled={loading || !file}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg font-medium transition-all">
            {loading ? (
              <span className="flex items-center gap-2"><span className="animate-spin">⏳</span> Analyzing...</span>
            ) : '🔍 Analyze'}
          </button>
        </div>

        {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-3 text-sm">{error}</div>}
      </div>

      {/* Report */}
      <div>
        {report ? (
          <div className="space-y-4">
            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
              <p className="text-sm text-slate-400 mb-1">Compliance Score</p>
              <div className={`text-5xl font-bold ${getScoreColor(report.score)}`}>{report.score}<span className="text-2xl">/100</span></div>
              <p className="text-slate-300 mt-3">{report.summary}</p>
            </div>

            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">⚠️ Gaps Found ({report.gaps?.length || 0})</h3>
              <div className="space-y-2">
                {report.gaps?.map((g, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${getSeverityColor(g.severity)}`}>
                    <div className="flex justify-between items-start">
                      <p className="font-medium">{g.area}</p>
                      <span className="text-xs uppercase font-bold">{g.severity}</span>
                    </div>
                    <p className="text-sm opacity-80 mt-1">{g.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">📋 Action Plan ({report.actionPlan?.length || 0})</h3>
              <div className="space-y-2">
                {report.actionPlan?.map((a, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 bg-slate-700/50 rounded-lg">
                    <span className="bg-blue-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center mt-0.5 shrink-0">{i + 1}</span>
                    <div className="flex-1">
                      <p className="text-white">{a.action}</p>
                      <div className="flex gap-2 mt-1 flex-wrap">
                        <span className={`text-xs px-2 py-0.5 rounded ${a.priority === 'high' ? 'bg-red-500/20 text-red-400' : a.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-blue-500/20 text-blue-400'}`}>{a.priority}</span>
                        <span className="text-xs text-slate-500">🕐 {a.timeline}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full min-h-[400px] border border-slate-700 border-dashed rounded-xl text-slate-500">
            <div className="text-4xl mb-3">📷</div>
            <p>Upload a room photo to see the compliance report</p>
          </div>
        )}
      </div>
    </div>
  )
}