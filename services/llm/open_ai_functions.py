import openai
import time
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL, AI_ROLE_TRIAL_SHORT_BACKUP
from .llm_eval_data import log_eval_data


client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_response_from_openai(user_prompt, resources="No resources provided.", model="gpt-5-mini"):

    # Specify the model to use
    model = model

    if model not in ["gpt-5-mini", "gpt-4o-mini", "gpt-4.1-mini"]:
        logger.error(f"Model {model} is not supported. Supported models are: gpt-5-mini, gpt-4o-mini, gpt-4.1-mini.")
        return "Error: Unsupported model selected."

    # Generate a response using the OpenAI API
    t0 = time.perf_counter()

    prompt_input = [
                {"role": "system", "content": AI_ROLE_TRIAL_SHORT_BACKUP + resources},
                {"role": "user", "content": user_prompt}
            ]

    if model =="gpt-5-mini":
        response = client.responses.create(
            model=model,
            input=prompt_input,
            tools=[{"type": "web_search_preview"}],
            reasoning={"effort": "low"},
            text={"verbosity": "low"},
            max_output_tokens=1000
        )
    else:
        response = client.responses.create(
            model=model,
            input=prompt_input,
            tools=[{"type": "web_search_preview"}],
            temperature=0.2,
            max_output_tokens=1000
        )

    latency = time.perf_counter() - t0
    logger.info(f"OpenAI response latency: {latency:.2f} seconds")

    # Get usage information
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr(usage, "output_tokens", None) if usage else None
    total_tokens = getattr(usage, "total_tokens", None) if usage else None

    # Return the generated text
    answer = response.output_text
    logger.info(f"OpenAI response: {answer}")

    # Log evaluation data
    log_eval_data(
        model=model,
        prompt=prompt_input,
        output_text=answer,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency=latency
    )
    return answer, response


# print(get_response_from_openai("When is the meeting tomorrow?"))