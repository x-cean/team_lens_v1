import openai
from team_lens_v1.config import OPENAI_API_KEY
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
        max_tokens=150
    )

    # Return the generated text
    return response.choices[0].message.content


# print(get_response_from_openai("When is the meeting tomorrow?"))