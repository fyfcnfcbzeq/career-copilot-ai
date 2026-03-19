from pydantic import BaseModel
from typing import List

class JobRequest(BaseModel):
    job_description: str
    resume: str

class JobResponse(BaseModel):
    match_score: float
    missing_skills: List[str]
    improved_summary: str
    cover_letter: str