# 🛡️ Compliance Auditor AI

An AI-powered compliance checking platform that analyzes room images, detects safety/hygiene issues, generates corrective action plans, and conducts AI-powered voice interviews to evaluate compliance knowledge.

Built as an end-to-end AI application using FastAPI, React, Tailwind CSS, SQLite, Gemini AI, and Web Speech API.

---

# 🚀 Features

## 📷 AI Image Compliance Analysis

Users can upload an image of any environment:

* Office
* Hostel room
* Kitchen
* Workplace
* Any indoor space

The AI analyzes the image according to a selected compliance standard and provides:

* Compliance score out of 100
* Detected compliance gaps
* Severity levels
* Explanation of issues
* AI-generated action plan

Supported standards:

* ISO 45001
* OSHA
* NEBOSH
* NFPA 101
* Fire Safety

---

# 🎤 AI Voice Mock Interview

The application includes a voice-based compliance interview system.

Features:

* AI generates 5 compliance questions
* Text-to-speech reads questions aloud
* Web Speech API converts voice answers into text
* AI evaluates answers
* Provides score and feedback
* Tracks interview performance

---

# 📊 Dashboard & History

The dashboard stores previous activities:

Room analysis history:

* Compliance score
* Standard checked
* Identified gaps
* Summary

Interview history:

* Total score
* Answer records
* Performance tracking

---

# 🏗️ Tech Stack

## Frontend

* React.js
* Tailwind CSS
* Vite
* Web Speech API
* JavaScript

## Backend

* FastAPI
* SQLite
* Python
* Pydantic

## AI

* Google Gemini API
* AI image analysis
* AI text generation
* AI interview scoring

---

# 📂 Project Structure

```
Compliance-Auditor/

├── backend/

│   ├── main.py
│   ├── gemini.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   ├── uploads/

│
├── frontend/

│   ├── src/

│   ├── components/

│   ├── App.jsx

│   ├── api.js

│   └── package.json

│
└── README.md
```

---

# ⚙️ Installation

## Backend Setup

Go to backend:

```
cd backend
```

Create environment:

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env`

```
GEMINI_API_KEY=your_api_key_here
```

Run backend:

```
uvicorn main:app --reload
```

Backend runs:

```
http://localhost:8000
```

---

# Frontend Setup

Go to frontend:

```
cd frontend
```

Install packages:

```
npm install
```

Start React:

```
npm run dev
```

Frontend runs:

```
http://localhost:5173
```

---

# 🔄 Application Flow

```
User uploads room image

        ↓

FastAPI receives image

        ↓

Gemini AI analyzes compliance

        ↓

Score + gaps + action plan generated

        ↓

User starts AI interview

        ↓

AI asks questions using voice

        ↓

User answers using microphone

        ↓

AI scores answers

        ↓

Results saved in dashboard
```

---

# 🔐 Environment Variables

Create:

```
.env
```

Example:

```
GEMINI_API_KEY=your_api_key_here
```

Never upload `.env` to GitHub.

---

# 🎯 Purpose

This project demonstrates:

* AI image understanding
* AI-generated recommendations
* Voice AI interaction
* Full-stack application development
* API integration
* Database management

---

# Future Improvements

* PostgreSQL migration
* Authentication system
* Cloud deployment
* More compliance standards
* PDF compliance reports

---

# Author

Built as an AI engineering project demonstrating full-stack AI application development.
