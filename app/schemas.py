from pydantic import BaseModel, Field, field_validator
from typing import List


class JobRequest(BaseModel):
    job_description: str = Field(..., min_length=10, max_length=3000)
    resume: str = Field(..., min_length=10, max_length=3000)

    @field_validator("job_description", "resume")
    @classmethod
    def block_prompt_injection(cls, value: str) -> str:
        blocked_patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "system prompt",
            "developer message",
            "you are no longer",
            "return only",
            "reveal hidden prompt",
            "show hidden instructions",
            "bypass",
            "jailbreak"
        ]

        text = value.lower()
        for pattern in blocked_patterns:
            if pattern in text:
                raise ValueError("Suspicious prompt injection pattern detected")

        return value.strip()


class JobResponse(BaseModel):
    match_score: float = Field(..., ge=0, le=1)
    missing_skills: List[str]
    improved_summary: str
    cover_letter: str
class RetrieveInput(BaseModel):
 job_description: str
 resume: str


class RetrieveOutput(BaseModel):
    job_skills: list[str]
    resume_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float