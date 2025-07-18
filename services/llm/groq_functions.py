from groq import Groq
from team_lens_v1.config import GROQ_API_KEY
# from .prompt_settings import AI_ROLE


AI_ROLE = """
You are a helpful work assistant, 
good at finding work-related information from lots of documents and 
give simple, clear and professional answer.
"""


def get_response_from_deepseek(user_prompt):
    # Initialize the Groq client
    client = Groq(api_key=GROQ_API_KEY)


    # Specify the model to use
    # model = "llama-3.3-70b-versatile"
    model = "deepseek-r1-distill-llama-70b"

    # System's task
    system_prompt = AI_ROLE

    # User's request
    user_prompt = user_prompt

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content

# print(get_response_from_deepseek("When is the meeting tomorrow?"))