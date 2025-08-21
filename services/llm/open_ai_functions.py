import openai
import time
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL, AI_ROLE_TRIAL_SHORT_BACKUP


client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_response_from_openai(user_prompt, resources="No resources provided.", model="gpt-5-mini"):

    # Specify the model to use
    model = model

    if model not in ["gpt-5-mini", "gpt-4o-mini", "gpt-4.1-mini"]:
        logger.error(f"Model {model} is not supported. Supported models are: gpt-5-mini, gpt-4o-mini, gpt-4.1-mini.")
        return "Error: Unsupported model selected."

    # Generate a response using the OpenAI API
    t0 = time.perf_counter()

    if model =="gpt-5-mini":
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": AI_ROLE_TRIAL_SHORT_BACKUP + resources},
                {"role": "user", "content": user_prompt}
            ],
            tools=[{"type": "web_search_preview"}],
            reasoning={"effort": "low"},
            text={"verbosity": "low"},
            max_output_tokens=1000
        )
    else:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": AI_ROLE_TRIAL_SHORT_BACKUP + resources},
                {"role": "user", "content": user_prompt}
            ],
            tools=[{"type": "web_search_preview"}],
            temperature=0.3,
            max_output_tokens=600
        )

    latency = time.perf_counter() - t0
    logger.info(f"OpenAI response latency: {latency:.2f} seconds")

    usage = getattr(response, "usage", None)
    usage_dict = {
        "prompt_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
        "completion_tokens": getattr(usage, "completion_tokens", None) if usage else None,
        "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
    }

    # Return the generated text
    answer = response.output_text
    logger.info(f"OpenAI response: {answer}")
    return answer, response


# print(get_response_from_openai("When is the meeting tomorrow?"))