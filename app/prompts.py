def build_prompt(
    job_description: str,
    resume: str,
    retrieved_context: dict,
) -> str:
    return f"""
You are a professional HR assistant.

Evaluate how well the candidate matches the job description.

Use retrieved_context as the source of truth for:
- match_score
- missing_skills

Do not change these values.

Return ONLY valid JSON in this exact format:
{{
  "match_score": 0.0,
  "missing_skills": ["skill1", "skill2"],
  "improved_summary": "string",
  "cover_letter": "string"
}}

Rules:
- Output JSON only
- No markdown
- No explanations
- No extra text
- Do not invent skills
- improved_summary: 2-3 professional sentences
- cover_letter: 3-5 professional sentences

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}

RETRIEVED_CONTEXT:
job_skills: {retrieved_context["job_skills"]}
resume_skills: {retrieved_context["resume_skills"]}
matched_skills: {retrieved_context["matched_skills"]}
missing_skills: {retrieved_context["missing_skills"]}
match_score: {retrieved_context["match_score"]}
"""