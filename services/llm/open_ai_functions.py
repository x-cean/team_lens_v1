import openai
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL, AI_ROLE_TRIAL_SHORT_BACKUP


def get_response_from_openai(user_prompt, resources="No resources provided."):

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Specify the model to use
    model = "gpt-4o-mini"

    # Generate a response using the OpenAI API
    ### todo: use system prompt
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": AI_ROLE_TRIAL_SHORT_BACKUP + resources},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=600
    )

    # Return the generated text
    answer = response.choices[0].message.content
    logger.info(f"OpenAI response: {answer}")
    return answer


# print(get_response_from_openai("When is the meeting tomorrow?"))