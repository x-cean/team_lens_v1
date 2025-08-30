import openai
import time
from typing import List
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL, AI_ROLE_TRIAL_SHORT_BACKUP
from .llm_eval_data import log_eval_data


client = openai.OpenAI(api_key=OPENAI_API_KEY)


def add_user_prompt_and_resources(user_prompt, resources="No resources provided."):
    messages = [
        {"role": "system", "content": AI_ROLE_TRIAL_SHORT_BACKUP + resources},
        {"role": "user", "content": user_prompt}
    ]
    return messages


def update_messages(new_messages: List[dict], messages=None):
    if messages is None:
        messages = []
    messages.extend(new_messages)
    return messages


def get_response_from_openai(user_prompt, resources="No resources provided.", model="gpt-5-mini",
                             reasoning_effort="low", text_verbosity="low",
                             temperature=0.2, max_output_tokens=1000,
                             web_search_preview = True):
    """
    Get a response from OpenAI's GPT model, with optional web search preview and parameter settings
    Evaluation data is logged for analysis
    """
    # Specify the model to use
    model = model

    if model not in ["gpt-5-mini", "gpt-4o-mini", "gpt-4.1-mini"]:
        logger.error(f"Model {model} is not supported. Supported models are: gpt-5-mini, gpt-4o-mini, gpt-4.1-mini.")
        return "Error: Unsupported openai model selected."  ### todo: how to handle error properly?

    # Generate a response using the OpenAI API

    messages = add_resource_to_messages(resources, user_prompt)

    if model =="gpt-5-mini":

        if web_search_preview:
            tools = [{"type": "web_search_preview"}]
        else:
            tools = None

        model_setup = {
            "reasoning_effort": reasoning_effort,
            "text_verbosity": text_verbosity,
            "max_output_tokens": max_output_tokens,
            "tools": tools
        }

        t0 = time.perf_counter()

        response = client.responses.create(
            model=model,
            input=messages,
            tools=tools,
            reasoning={"effort": reasoning_effort},
            text={"verbosity": text_verbosity},
            max_output_tokens=max_output_tokens
        )

    else: # gpt-4o-mini and gpt-4.1-mini
        if web_search_preview:
            tools = [{"type": "web_search_preview"}]
        else:
            tools = None

        model_setup = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "tools": tools
        }

        t0 = time.perf_counter()

        response = client.responses.create(
            model=model,
            input=prompt_input,
            tools=tools,
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )

    latency = time.perf_counter() - t0
    logger.info(f"OpenAI response latency: {latency:.2f} seconds")

    # Get the response text
    answer = response.output_text
    logger.info(f"OpenAI response: {response}")

    # Get usage information
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr(usage, "output_tokens", None) if usage else None
    total_tokens = getattr(usage, "total_tokens", None) if usage else None

    # Log evaluation data
    log_eval_data(
        model=model,
        model_setup=model_setup,
        prompt=prompt_input,
        output_text=answer,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency=latency
    )

    # return output text for further use
    return answer




