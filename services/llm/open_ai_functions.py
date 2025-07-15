from dotenv import load_dotenv
import os

import openai


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def get_response_from_openai(user_prompt):

    client = openai.OpenAI(api_key=API_KEY)

    # Specify the model to use
    model = "gpt-4o-mini"

    # Generate a response using the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "assistant",
             "content": "You are a helpful work assistant, "
                        "good at finding work-related information from lots of documents"
                        "and give simple, clear and professional answer."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=2,
        max_tokens=150
    )

    # Return the generated text
    # print(response.choices[0].message.content)
    return response.choices[0].message.content


# get_response_from_openai("When is the meeting tomorrow?")