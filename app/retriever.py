import re
from typing import Any, Dict, List


KNOWN_SKILLS = [
    "python",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "docker",
    "kubernetes",
    "rest",
    "api",
    "git",
    "linux",
    "javascript",
    "react",
    "html",
    "css",
]


def normalize_text(text: str) -> str:
    return text.lower().strip()


def extract_skills(text: str) -> List[str]:
    text = normalize_text(text)
    found_skills: List[str] = []

    for skill in KNOWN_SKILLS:
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))

def retrieve_data(job_description: str, resume: str) -> Dict[str, Any]:
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume)

    matched_skills = sorted(list(set(job_skills) & set(resume_skills)))
    missing_skills = sorted(list(set(job_skills) - set(resume_skills)))

    if not job_skills:
        match_score = 0.0
    else:
        match_score = round(len(matched_skills) / len(job_skills), 2)

    return {
        "job_skills": job_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
    }
def retrieve_tool(input_data: dict) -> dict:
    result = retrieve_data(
        input_data["job_description"],
        input_data["resume"]
    )
    return result