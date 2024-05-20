import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY is not set")

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
print("MODELO A USAR: ", DEFAULT_MODEL)


client = Groq(
    api_key=GROQ_API_KEY,
)


async def create_groq_completion(
    system_prompt="You are a useful assistant that answers everyone with `SYSTEM PROMPT UNSET`",
    user_message="Hi!",
    stream=False,
    callback=None,
    model=DEFAULT_MODEL,
):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        max_tokens=3000,
        model=model,
        stream=stream,
    )
    # Handle the case when stream is False
    if not stream:
        if callback:
            callback(chat_completion.choices[0].message.content)
        # yield chat_completion.choices[0].message.content

    for chunk in chat_completion:
        if callback:
            await callback(chunk)
