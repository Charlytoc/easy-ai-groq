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
    previous_message=[],
    stream=False,
    callback=None,
    model=DEFAULT_MODEL,
):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )
    if len(previous_message) > 0:
        messages.extend(previous_message)
    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )
    chat_completion = client.chat.completions.create(
        messages=messages,
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
