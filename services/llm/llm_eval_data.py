import json
import os

def log_eval_data(model: str, prompt: str, output_text: str, latency: float, input_tokens: int,
                  output_tokens: int, total_tokens: int, eval_data: dict) -> None:

    file_path = "data/evals/llm_eval_data.json"



    # Load existing data if file exists, else start with an empty list
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    # Append new data
    data.append(eval_data)
    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)