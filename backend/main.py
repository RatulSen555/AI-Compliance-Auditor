from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import json, os
from database import get_db, init_db
from gemini import analyze_image, generate_questions, score_answer

app = FastAPI(title="Compliance Auditor API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
init_db()


@app.get("/")
def health():
    return {"status": "ok", "message": "Compliance Auditor API is running"}


@app.get("/api/status")
def api_status():
    from gemini import _use_gemini, API_KEY
    return {
        "gemini_active": _use_gemini,
        "has_api_key": bool(API_KEY),
        "mode": "Gemini AI" if _use_gemini else "Mock (add GEMINI_API_KEY to .env for real AI)"
    }


@app.post("/analyze")
async def analyze_room(file: UploadFile = File(...), standard: str = Form(...)):
    image_bytes = await file.read()
    mime_type = file.content_type or "image/jpeg"
    image_path = f"uploads/{file.filename}"
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    result = analyze_image(image_bytes, mime_type, standard)

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO compliance_checks (image_path, standard, score, gaps, action_plan, summary) VALUES (?,?,?,?,?,?)",
        (image_path, standard, result["score"], json.dumps(result["gaps"]), json.dumps(result["actionPlan"]), result["summary"])
    )
    conn.commit()
    check_id = cursor.lastrowid
    conn.close()

    return {"id": check_id, **result}


@app.post("/interview/generate")
async def start_interview(standard: str = "ISO 45001"):
    data = generate_questions(standard)
    questions = data["questions"]

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO interview_sessions (standard, questions, answers, total_score) VALUES (?,?,?,?)",
        (standard, json.dumps(questions), json.dumps([]), 0)
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()

    return {"session_id": session_id, "questions": questions}


@app.post("/interview/score")
async def score_interview_answer(
    session_id: int = Form(...),
    question_index: int = Form(...),
    question: str = Form(...),
    answer: str = Form(...),
    expected_topics: str = Form(...)
):
    topics = json.loads(expected_topics)
    result = score_answer(question, answer, topics)

    conn = get_db()
    row = conn.execute("SELECT * FROM interview_sessions WHERE id=?", (session_id,)).fetchone()
    answers = json.loads(row["answers"])
    total = row["total_score"]

    answers.append({
        "question": question,
        "answer": answer,
        "score": result["score"],
        "feedback": result["feedback"]
    })
    total += result["score"]

    conn.execute("UPDATE interview_sessions SET answers=?, total_score=? WHERE id=?",
                 (json.dumps(answers), total, session_id))
    conn.commit()
    conn.close()

    return {
        "score": result["score"],
        "feedback": result["feedback"],
        "missedPoints": result["missedPoints"],
        "total_so_far": total
    }


@app.get("/history")
async def get_history():
    conn = get_db()
    checks = conn.execute("SELECT * FROM compliance_checks ORDER BY created_at DESC LIMIT 50").fetchall()
    interviews = conn.execute("SELECT * FROM interview_sessions ORDER BY created_at DESC LIMIT 20").fetchall()
    conn.close()

    return {
        "checks": [dict(r) for r in checks],
        "interviews": [dict(r) for r in interviews]
    }