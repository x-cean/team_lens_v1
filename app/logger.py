import logging
import sys
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler("../project.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("team_lens_v1")

# Dedicated logger for LLM evaluation my_data written as JSON lines
# We lazily configure it to avoid duplicate handlers on reloads.

def _setup_llm_eval_logger() -> None:
    llm_logger = logging.getLogger("llm_eval")
    if getattr(llm_logger, "_configured", False):
        return

    llm_logger.setLevel(logging.INFO)
    llm_logger.propagate = False  # don't mirror into root handlers

    # Resolve path to my_data/evals/llm_eval_data.json relative to this file
    base_dir = os.path.dirname(__file__)
    evals_dir = os.path.join(base_dir, "my_data", "evals")
    os.makedirs(evals_dir, exist_ok=True)
    eval_file = os.path.join(evals_dir, "llm_eval_data.json")

    fh = logging.FileHandler(eval_file, mode="a", encoding="utf-8")
    # Formatter writes only the message (which will be a JSON string), one per line
    fh.setFormatter(logging.Formatter("%(message)s"))
    llm_logger.addHandler(fh)

    # Mark as configured to prevent duplicate handlers
    setattr(llm_logger, "_configured", True)


def get_llm_eval_logger() -> logging.Logger:
    """Return the dedicated logger for LLM eval my_data (JSON lines)."""
    _setup_llm_eval_logger()
    return logging.getLogger("llm_eval")