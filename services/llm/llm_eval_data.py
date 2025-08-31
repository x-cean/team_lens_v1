import json
from team_lens_v1.logger import get_llm_eval_logger


def log_eval_data(model: str, model_setup: dict, prompt: str | list, output_text: str, latency: float, input_tokens: int,
                  output_tokens: int, total_tokens: int) -> None:
    """
    Log LLM evaluation data to a JSON file via Python logging.
    Appends one JSON object per line into team_lens_v1/data/evals/llm_eval_data.json
    to avoid rewriting whole files and reduce dev autoreload churn.
    """
    logger = get_llm_eval_logger()

    eval_data_dict = {
        "model": model,
        "model_setup": model_setup,
        "prompt": prompt,
        "output_text": output_text,
        "latency": latency,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }

    # Emit as a single JSON line
    logger.info(json.dumps(eval_data_dict, ensure_ascii=False))