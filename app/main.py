from fastapi import FastAPI
from app.schemas import JobRequest, JobResponse
from app.llm import generate_response

app = FastAPI(title="Career Copilot AI")


@app.post("/analyze-job", response_model=JobResponse)
def analyze_job(request: JobRequest):
    return generate_response(request.job_description, request.resume)