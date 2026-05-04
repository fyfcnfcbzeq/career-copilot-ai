import os
from typing import Any
import json
import re
from openai import OpenAI
from app.schemas import JobResponse
from app.retriever import retrieve_data
from app.prompts import build_prompt
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)


def extract_json_block(text: str) -> dict | None:
    if not text:
        return None

    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        try:
            return json.loads(fenced_match.group(1))
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        candidate = text[start:end]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def get_raw_text(completion) -> str:
    output_text = getattr(completion, "output_text", None)
    if output_text:
        return output_text

    output = getattr(completion, "output", None)
    if output:
        try:
            chunks = []
            for item in output:
                content_list = getattr(item, "content", None)
                if not content_list:
                    continue
                for part in content_list:
                    text = getattr(part, "text", None)
                    if text:
                        chunks.append(text)
            return "\n".join(chunks).strip()
        except Exception:
            pass

    return ""


def generate_response(job_description: str, resume: str) -> dict:
    print("=== GENERATE_RESPONSE STARTED ===")
    print("JOB DESCRIPTION:", job_description)
    print("RESUME:", resume)
    tools: list[Any] = [
    {
        "type": "function",
        "name": "retrieve_tool",
        "description": "Extract skills from job description and resume, compare them, and calculate match score.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_description": {"type": "string"},
                "resume": {"type": "string"}
            },
            "required": ["job_description", "resume"],
            "additionalProperties": False
        }
    }
]


    try:
        # Первый вызов модели: даем ей возможность выбрать tool
        completion = client.responses.create(
    model=os.getenv("MODEL_NAME") or "gpt-oss-120b",
    input=f"""
You are an HR assistant.

You must use the available tool retrieve_tool before generating the final answer.

The user provided:
job_description: {job_description}
resume: {resume}

After calling the tool, return valid JSON with:
- match_score
- missing_skills
- improved_summary
- cover_letter
""",
    tools=tools,
    tool_choice="auto"
)
        print("=== FIRST MODEL CALL DONE ===")
        print("COMPLETION OUTPUT:", getattr(completion, "output", None))

        retrieval_result = None

        # Пытаемся найти вызов инструмента в ответе модели
        output_items = getattr(completion, "output", None)

        if output_items:
            for item in output_items:
                item_type = getattr(item, "type", None)

                if item_type == "function_call":
                    tool_name = getattr(item, "name", None)
                    arguments = getattr(item, "arguments", "{}")
                    print("=== FUNCTION CALL FOUND ===")
                    print("TOOL NAME:", tool_name)
                    print("TOOL ARGUMENTS:", arguments)

                    if tool_name == "retrieve_tool":
                        try:
                            args = json.loads(arguments)
                        except Exception:
                            args = {
                                "job_description": job_description,
                                "resume": resume
                            }

                        retrieval_result = retrieve_data(
                            args["job_description"],
                            args["resume"]
                        )
                        print("=== TOOL EXECUTED ===")
                        print("TOOL RESULT:", retrieval_result)
                        break

        # Если модель tool не вызвала, вызываем сами
        if retrieval_result is None:
            print("=== TOOL WAS NOT CALLED BY MODEL ===")
            print("USING DIRECT FALLBACK CALL")
            retrieval_result = retrieve_data(job_description, resume)
            print("FALLBACK RESULT:", retrieval_result)
        # Строим prompt уже на основе результата ретривера
        prompt = build_prompt(
            job_description=job_description,
            resume=resume,
            retrieved_context=retrieval_result,
        )

        # Второй вызов модели: просим сгенерировать финальный ответ
        completion = client.responses.create(
            model=os.getenv("MODEL_NAME") or "gpt-oss-120b",
            input=prompt,
        )

        raw_text = get_raw_text(completion)

        if not raw_text:
            return {
                "match_score": retrieval_result["match_score"],
                "missing_skills": retrieval_result["missing_skills"],
                "improved_summary": "LLM returned empty response",
                "cover_letter": "LLM returned empty response",
            }

        data = extract_json_block(raw_text)

        if data is None:
            return {
                "match_score": retrieval_result["match_score"],
                "missing_skills": retrieval_result["missing_skills"],
                "improved_summary": "Invalid model output format",
                "cover_letter": "Invalid model output format",
            }

        if "match_score" not in data:
            data["match_score"] = retrieval_result["match_score"]

        if "missing_skills" not in data:
            data["missing_skills"] = retrieval_result["missing_skills"]

        validated = JobResponse(**data)
        print("=== FINAL VALIDATED RESPONSE ===")
        print(validated.model_dump())
        return validated.model_dump()

    except Exception as e:
        print("=== ERROR IN GENERATE_RESPONSE ===")
        print(str(e))
        return {
            "match_score": 0.0,
            "missing_skills": [],
            "improved_summary": f"Protected fallback: {str(e)}",
            "cover_letter": f"Protected fallback: {str(e)}",
        }
