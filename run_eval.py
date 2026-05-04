import json
import csv
from app.retriever import retrieve_data

DATASET_PATH = "dataset.json"
RESULTS_PATH = "retriever_results.csv"


def calculate_metrics(expected_skills, predicted_skills):
    expected = set(skill.lower() for skill in expected_skills)
    predicted = set(skill.lower() for skill in predicted_skills)

    true_positive = len(expected & predicted)

    precision = true_positive / len(predicted) if predicted else 0.0
    recall = true_positive / len(expected) if expected else 0.0

    return round(precision, 2), round(recall, 2)


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:
        job_description = item["job_description"]
        resume = item["resume"]
        expected_skills = item["expected_skills"]

        retrieval_result = retrieve_data(job_description, resume)

        # Для оценки ретривера здесь берем навыки, извлеченные из вакансии
        predicted_skills = retrieval_result["job_skills"]

        precision, recall = calculate_metrics(expected_skills, predicted_skills)

        results.append({
            "job_description": job_description,
            "resume": resume,
            "expected_skills": ", ".join(expected_skills),
            "predicted_skills": ", ".join(predicted_skills),
            "precision": precision,
            "recall": recall,
        })

    with open(RESULTS_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "job_description",
                "resume",
                "expected_skills",
                "predicted_skills",
                "precision",
                "recall",
            ],
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Готово! {RESULTS_PATH} создан")



if __name__ == "__main__":
    main()