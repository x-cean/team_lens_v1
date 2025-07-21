import openai
from team_lens_v1.config import OPENAI_API_KEY
# from .prompt_settings import AI_ROLE


AI_ROLE = """
You are a helpful work assistant, 
good at finding work-related information from lots of documents and 
give simple, clear and professional answer.
"""


def get_response_from_openai(user_prompt):

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Specify the model to use
    model = "gpt-4o-mini"

    # Generate a response using the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "assistant", "content": AI_ROLE},
            {"role": "user", "content": user_prompt}
        ],
        temperature=2,
        max_tokens=150
    )

    # Return the generated text
    return response.choices[0].message.content


print(get_response_from_openai("When is the meeting tomorrow?"))