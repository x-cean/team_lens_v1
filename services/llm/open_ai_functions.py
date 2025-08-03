import openai
from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger
from .prompt_settings import AI_ROLE_TRIAL


def get_response_from_openai(user_prompt, resources="No resources provided."):

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Specify the model to use
    model = "gpt-4o-mini"

    # Generate a response using the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "assistant", "content": AI_ROLE_TRIAL + resources},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5, # setting to 2 cause multi language weird answers
        max_tokens=600
    )

    # Return the generated text
    answer = response.choices[0].message.content
    # if "```" in answer:
    #     answer = answer.replace("```", "")
    # elif "```html" in answer:
    #     answer = answer.replace("```html", "")
    # elif "html" in answer[:5]:
    #     answer = answer.replace("html", "")
    if answer.startswith("```html"):
        answer = answer[7:]
    if answer.endswith("```"):
        answer = answer[:-3]
    logger.info(f"OpenAI response: {answer}")
    return answer


# print(get_response_from_openai("When is the meeting tomorrow?"))