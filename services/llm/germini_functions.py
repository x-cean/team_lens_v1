from team_lens_v1.config import GERMINI_API_KEY
from google import genai
# from .prompt_settings import AI_ROLE


AI_ROLE = """
You are a helpful work assistant, 
good at giving simple, clear and professional answer.
Please answer question using the following information.
If no information given, be honest, search the internet and give general answer.
Following are the resources.
"""


def get_response_from_germini(resources, user_prompt): # from google import genai
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=GERMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=AI_ROLE + resources + "Question: " + user_prompt
    )
    # print(response.text)
    return response.text


# print(get_response_from_germini("When is the meeting tomorrow?"))