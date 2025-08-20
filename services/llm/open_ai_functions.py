import openai
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL, AI_ROLE_TRIAL_SHORT_BACKUP


def get_response_from_openai(user_prompt, resources="No resources provided.", model="gpt-5-mini"):

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Specify the model to use
    model = model

    if model not in ["gpt-5-mini", "gpt-4o-mini", "gpt-4.1-mini"]:
        logger.error(f"Model {model} is not supported. Supported models are: gpt-5-mini, gpt-4o-mini, gpt-4.1-mini.")
        return "Error: Unsupported model selected."

    # Generate a response using the OpenAI API
    elif model =="gpt-5-mini":
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

    # Return the generated text
    answer = response.output_text
    logger.info(f"OpenAI response: {answer}")
    return answer


# print(get_response_from_openai("When is the meeting tomorrow?"))