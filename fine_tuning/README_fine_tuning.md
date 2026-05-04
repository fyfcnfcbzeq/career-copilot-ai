# Fine-tuning pipeline for Career Copilot AI

## Task

The goal is to adapt an LLM for the Career Copilot AI project.

The model should receive:

job_description
resume

and return only valid JSON with:

match_score
missing_skills
improved_summary
cover_letter

## Current project baseline

The current Career Copilot AI project uses:

FastAPI API endpoint `/analyze-job`
Pydantic schemas for request and response validation
retriever.py for skill extraction and match_score calculation
llm.py for final response generation

## Fine-tuning strategy

The selected strategy is supervised fine-tuning with LoRA.

LoRA is selected because full fine-tuning is too expensive for the current project resources. LoRA allows training adapter weights instead of the full model.

## Dataset format

The dataset is prepared in JSONL chat format.

Each row contains:

system instruction
user message with job description and resume
assistant message with the expected JSON output

## Models for comparison

The planned models are:

1. Qwen2.5-0.5B-Instruct
2. TinyLlama-1.1B-Chat
3. Phi-3-mini

The primary choice for the first local experiment is Qwen2.5-0.5B-Instruct with LoRA.

## Metrics

The planned evaluation metrics are:

JSON validity
missing_skills precision
missing_skills recall
missing_skills F1
match_score error
manual quality check for improved_summary and cover_letter

## Limitation

The main FastAPI project is not changed. Fine-tuning files are placed in a separate folder to avoid breaking the working API.