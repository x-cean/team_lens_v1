from team_lens_v1.config import GERMINI_API_KEY
from google import genai
# from .prompt_settings import AI_ROLE

AI_ROLE_CORE = """
You are a helpful work assistant, 
good at giving simple, clear and professional answer.
The following text pieces were a search result from the user's files based on their question.
Please answer their question using them as first level resources.
If no information was given, or no relevant info was found in those references, 
be honest, search the internet and give general answer.
Following are the resources.
"""

AI_ROLE_TRIAL = """
You are a helpful work assistant, 
good at giving simple, clear and professional answer.
User gives us a file, we searched relevant info in that file based on their question.
The following text pieces were a search result based on similarity comparison. 
They are from the same file, but not necessarily continuous.
Please answer their question using them resources.
If no information was given, or no relevant info was found in those references, 
be honest, search the internet and give general answer.
Following are the resources.
"""


def get_response_from_germini(resources, user_prompt): # from google import genai
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=GERMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=AI_ROLE_TRIAL + resources + "User question: " + user_prompt
    )
    # print(response.text)
    return response.text


# print(get_response_from_germini("When is the meeting tomorrow?"))