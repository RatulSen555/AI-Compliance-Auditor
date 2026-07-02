import { useState, useRef } from 'react'
import { generateInterview, scoreAnswer } from '../api'

export default function Interview() {
  const [standard, setStandard] = useState('ISO 45001')
  const [sessionId, setSessionId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [qIndex, setQIndex] = useState(0)
  const [phase, setPhase] = useState('setup')
  const [transcript, setTranscript] = useState('')
  const [currentResult, setCurrentResult] = useState(null)
  const [scores, setScores] = useState([])
  const [totalScore, setTotalScore] = useState(0)
  const [loading, setLoading] = useState(false)
  const [listening, setListening] = useState(false)
  const recognitionRef = useRef(null)

  const startInterview = async () => {
    setLoading(true)
    try {
      const data = await generateInterview(standard)
      setSessionId(data.session_id)
      setQuestions(data.questions)
      setQIndex(0)
      setScores([])
      setTotalScore(0)
      setCurrentResult(null)
      setTranscript('')
      setPhase('speaking')
      setTimeout(() => speakQuestion(data.questions[0].question), 500)
    } catch (err) {
      alert('Failed: ' + err.message)
    }
    setLoading(false)
  }

  const speakQuestion = (text) => {
    window.speechSynthesis.cancel()
    const utter = new SpeechSynthesisUtterance(text)
    utter.rate = 0.9
    utter.pitch = 1
    utter.onend = () => setPhase('listening')
    window.speechSynthesis.speak(utter)
  }

  const startListening = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) {
      alert('Speech Recognition not supported. Use Google Chrome.')
      return
    }
    const recognition = new SR()
    recognition.lang = 'en-US'
    recognition.interimResults = true
    recognition.continuous = false

    recognition.onresult = (e) => {
      const t = Array.from(e.results).map(r => r[0].transcript).join('')
      setTranscript(t)
    }

    recognition.onend = () => {
      setListening(false)
      if (recognitionRef.current && recognitionRef.current.results) {
        const final = Array.from(recognitionRef.current.results)
          .filter(r => r.isFinal)
          .map(r => r[0].transcript)
          .join('')
        if (final.trim()) {
          setTranscript(final)
          setPhase('feedback')
          submitAnswer(final)
        }
      }
    }

    recognition.onerror = (e) => {
      setListening(false)
      if (e.error === 'no-speech' || e.error === 'aborted') return
      console.error('Speech error:', e.error)
    }

    recognitionRef.current = recognition
    recognition.start()
    setListening(true)
  }

  const submitAnswer = async (answerText) => {
    try {
      const q = questions[qIndex]
      const result = await scoreAnswer(sessionId, qIndex, q.question, answerText, q.expectedTopics)
      setCurrentResult(result)
      setTotalScore(result.total_so_far)
      setScores(prev => [...prev, result.score])
    } catch (err) {
      setCurrentResult({ score: 0, feedback: 'Error: ' + err.message, missedPoints: [] })
    }
  }

  const nextQuestion = () => {
    window.speechSynthesis.cancel()
    if (qIndex + 1 >= questions.length) {
      setPhase('done')
      return
    }
    const next = qIndex + 1
    setQIndex(next)
    setTranscript('')
    setCurrentResult(null)
    setPhase('speaking')
    setTimeout(() => speakQuestion(questions[next].question), 300)
  }

  const reset = () => {
    window.speechSynthesis.cancel()
    if (recognitionRef.current) try { recognitionRef.current.abort() } catch(e) {}
    setPhase('setup')
    setQuestions([])
    setScores([])
    setTotalScore(0)
    setTranscript('')
    setCurrentResult(null)
    setSessionId(null)
    setListening(false)
  }

  const handleManualSubmit = () => {
    if (!transcript.trim()) return
    setPhase('feedback')
    submitAnswer(transcript)
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {phase === 'setup' && (
        <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 text-center space-y-6">
          <div className="text-5xl">🎤</div>
          <h2 className="text-2xl font-bold text-white">Compliance Voice Interview</h2>
          <p className="text-slate-400 max-w-md mx-auto">AI asks 5 compliance questions via voice. Answer verbally or type. Get scored in real-time.</p>
          <select value={standard} onChange={e => setStandard(e.target.value)}
            className="bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white w-full max-w-xs focus:outline-none focus:border-blue-500">
            <option>ISO 45001</option>
            <option>OSHA</option>
            <option>NEBOSH</option>
            <option>NFPA 101</option>
            <option>Fire Safety</option>
          </select>
          <button onClick={startInterview} disabled={loading}
            className="px-8 py-4 bg-green-600 hover:bg-green-700 disabled:opacity-50 rounded-xl text-lg font-bold transition-all cursor-pointer">
            {loading ? '⏳ Generating questions...' : '🚀 Start Interview'}
          </button>
        </div>
      )}

      {(phase === 'speaking' || phase === 'listening' || phase === 'feedback') && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm text-slate-400 mb-1">
            <span>Question {qIndex + 1} of {questions.length}</span>
            <span>Score: {totalScore}/100</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${((qIndex + (phase === 'feedback' ? 1 : 0)) / questions.length) * 100}%` }} />
          </div>

          <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center gap-2 mb-3">
              <span className={`w-3 h-3 rounded-full ${phase === 'speaking' ? 'bg-blue-500 animate-pulse' : phase === 'listening' ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`} />
              <span className="text-sm text-slate-400">
                {phase === 'speaking' ? 'AI is asking...' : phase === 'listening' ? '🎤 Listening... (speak now or type below)' : '✅ Scored!'}
              </span>
              <span className="ml-auto text-xs px-2 py-1 rounded bg-slate-700 text-slate-400">{questions[qIndex]?.difficulty}</span>
            </div>
            <p className="text-lg text-white leading-relaxed">{questions[qIndex]?.question}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {questions[qIndex]?.expectedTopics?.map((t, i) => (
                <span key={i} className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-400">{t}</span>
              ))}
            </div>
          </div>

          {(phase === 'listening' || phase === 'feedback') && (
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700 space-y-3">
              <p className="text-xs text-slate-500">Your answer {phase === 'listening' ? '(speaking or typing):' : ':'}</p>
              <textarea
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                disabled={phase === 'feedback'}
                rows={3}
                className="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-blue-500 resize-none disabled:opacity-60"
                placeholder="Your answer will appear here as you speak, or type it manually..."
              />
              {phase === 'listening' && (
                <div className="flex gap-3">
                  <button onClick={startListening} disabled={listening}
                    className={`flex-1 py-3 rounded-lg font-medium transition-all cursor-pointer ${listening ? 'bg-red-600/50 text-red-300' : 'bg-red-600 hover:bg-red-700 text-white'}`}>
                    {listening ? '🔴 Listening...' : '🎤 Start Speaking'}
                  </button>
                  <button onClick={handleManualSubmit} disabled={!transcript.trim()}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 rounded-lg font-medium transition-all cursor-pointer">
                    Submit Answer
                  </button>
                </div>
              )}
            </div>
          )}

          {phase === 'feedback' && currentResult && (
            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Score for this answer:</span>
                <span className={`text-4xl font-bold ${currentResult.score >= 15 ? 'text-green-400' : currentResult.score >= 10 ? 'text-yellow-400' : 'text-red-400'}`}>
                  {currentResult.score}<span className="text-lg">/20</span>
                </span>
              </div>
              <p className="text-slate-300 leading-relaxed">{currentResult.feedback}</p>
              {currentResult.missedPoints?.length > 0 && (
                <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                  <p className="text-sm text-red-400 font-medium mb-1">Missed topics:</p>
                  <ul className="list-disc list-inside text-sm text-slate-400">
                    {currentResult.missedPoints.map((p, i) => <li key={i}>{p}</li>)}
                  </ul>
                </div>
              )}
              <button onClick={nextQuestion}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all cursor-pointer">
                {qIndex + 1 >= questions.length ? '🎯 See Final Results' : `➡️ Next Question (${qIndex + 2}/${questions.length})`}
              </button>
            </div>
          )}
        </div>
      )}

      {phase === 'done' && (
        <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 text-center space-y-6">
          <div className="text-5xl">🏆</div>
          <h2 className="text-2xl font-bold text-white">Interview Complete!</h2>
          <div className={`text-6xl font-bold ${totalScore >= 75 ? 'text-green-400' : totalScore >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
            {totalScore}<span className="text-2xl">/100</span>
          </div>
          <div className="flex justify-center gap-3">
            {scores.map((s, i) => (
              <div key={i} className="bg-slate-700 rounded-lg px-4 py-3 text-center min-w-[70px]">
                <p className="text-xs text-slate-400 mb-1">Q{i + 1}</p>
                <p className={`text-xl font-bold ${s >= 15 ? 'text-green-400' : s >= 10 ? 'text-yellow-400' : 'text-red-400'}`}>{s}</p>
                <p className="text-xs text-slate-500">/20</p>
              </div>
            ))}
          </div>
          <button onClick={reset} className="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all cursor-pointer">
            🔄 Try Again
          </button>
        </div>
      )}
    </div>
  )
}