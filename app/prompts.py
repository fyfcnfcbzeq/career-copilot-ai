def build_prompt(job_description: str, resume: str) -> str:
    return f"""
You are an AI career assistant.

Analyze the job description and the candidate resume.

Return ONLY valid JSON in this format:
{{
  "match_score": 0.0,
  "missing_skills": [],
  "improved_summary": "",
  "cover_letter": ""
}}

Job Description:
{job_description}

Resume:
{resume}
"""