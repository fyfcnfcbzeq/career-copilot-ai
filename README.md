# Career Copilot AI

AI-powered API that analyzes a resume against a job description and returns structured JSON output.

---

## 🚀 API Features

- Match score between resume and job description
- Missing skills detection
- Improved resume summary
- Cover letter generation

---

## 🛠 Tech Stack

- Python
- FastAPI
- OpenAI-compatible API (OpenRouter)
- Pydantic

---

## ⚙️ How to run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open in browser:

http://127.0.0.1:8000/docs

---

## 📌 Example request

```json
{
  "job_description": "Looking for a Python developer with FastAPI and Docker experience",
  "resume": "Python developer with experience in machine learning and APIs"
}
```

---

## 📌 Example response

```json
{
  "match_score": 0.7,
  "missing_skills": ["FastAPI", "Docker"],
  "improved_summary": "...",
  "cover_letter": "..."
}
```

---

## 🤖 LLM Integration

The application connects to an OpenAI-compatible API via OpenRouter and generates structured JSON responses with controlled temperature.

---

# 💡 Project Idea (Task 1)

The goal of this project is to build an AI-powered career assistant that helps users improve their job applications.

The system analyzes job descriptions and resumes to provide structured insights and personalized recommendations.

Planned features include:

- Resume optimization
- Cover letter generation
- Skill gap analysis
- Job matching

---

## 📌 Status

Project in progress
