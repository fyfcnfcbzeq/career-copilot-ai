import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.prompts import build_prompt

load_dotenv(dotenv_path=".env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_response(job_description: str, resume: str):
    prompt = build_prompt(job_description, resume)

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content

        if content is None:
            return {
                "match_score": 0.0,
                "missing_skills": [],
                "improved_summary": "Empty response from LLM",
                "cover_letter": "Empty response from LLM"
            }

        content = content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(content)
        except Exception:
            return {
                "match_score": 0.0,
                "missing_skills": [],
                "improved_summary": content,
                "cover_letter": content
            }

        return {
            "match_score": float(data.get("match_score", 0.0)),
            "missing_skills": data.get("missing_skills", []),
            "improved_summary": str(data.get("improved_summary", "")),
            "cover_letter": str(data.get("cover_letter", ""))
        }

    except Exception as e:
        return {
            "match_score": 0.0,
            "missing_skills": [],
            "improved_summary": f"LLM error: {str(e)}",
            "cover_letter": f"LLM error: {str(e)}"
        }