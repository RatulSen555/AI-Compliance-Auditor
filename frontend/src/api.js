const API = '/api'

export async function analyzeRoom(file, standard) {
  const form = new FormData()
  form.append('file', file)
  form.append('standard', standard)
  const res = await fetch(`${API}/analyze`, { method: 'POST', body: form })
  if (!res.ok) throw new Error('Analysis failed')
  return res.json()
}

export async function generateInterview(standard) {
  const res = await fetch(`${API}/interview/generate?standard=${encodeURIComponent(standard)}`, {
    method: 'POST'
  })
  if (!res.ok) throw new Error('Failed to generate questions')
  return res.json()
}

export async function scoreAnswer(sessionId, questionIndex, question, answer, expectedTopics) {
  const form = new FormData()
  form.append('session_id', sessionId)
  form.append('question_index', questionIndex)
  form.append('question', question)
  form.append('answer', answer)
  form.append('expected_topics', JSON.stringify(expectedTopics))
  const res = await fetch(`${API}/interview/score`, { method: 'POST', body: form })
  if (!res.ok) throw new Error('Failed to score answer')
  return res.json()
}

export async function getHistory() {
  const res = await fetch(`${API}/history`)
  if (!res.ok) throw new Error('Failed to load history')
  return res.json()
}