from fastapi import FastAPI
from app.schemas import JobRequest, JobResponse
from app.llm import generate_response

app = FastAPI(
    title="Career Copilot AI",
    description="AI-powered API for job analysis",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/analyze-job", response_model=JobResponse)
def analyze_job(data: JobRequest):
    return generate_response(data.job_description, data.resume)