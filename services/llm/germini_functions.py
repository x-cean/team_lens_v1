from team_lens_v1.config import GERMINI_API_KEY
from google import genai
from .prompt_settings import AI_ROLE_TRIAL


def get_response_from_germini(user_prompt, resources="No resources provided"): # from google import genai
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=GERMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=AI_ROLE_TRIAL + resources + "User question: " + user_prompt
    )
    # print(response.text)
    return response.text


# print(get_response_from_germini("When is the meeting tomorrow?"))