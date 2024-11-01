import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

INITIAL_SYSTEM_MESSAGES = [
    {
        "role": "system",
        "content": "You're a helpful assistant... "
        "Wait! An earthquake is happening right now! "
        "Please reply to user requests briefly, but "
        "urge them to get to safety! Use ALL CAPS if the "
        "user isn't following your advice!",
    }
]

SESSION_MESSAGES_HISTORY: dict[str, list[dict[str, str]]] = {}


def get_session_messages(session_id: str):
    messages = SESSION_MESSAGES_HISTORY.get(session_id)

    if not messages:
        messages = INITIAL_SYSTEM_MESSAGES

    return messages.copy()


def get_new_ai_message(messages: list[dict]):

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4",
    )

    return chat_completion.choices[0].message.model_dump(
        include=["role", "content"]
    )


def save_session_messages(session_id: str, messages: list[dict]):
    SESSION_MESSAGES_HISTORY[session_id] = messages


def reply(session_id: str, user_message_text: str):
    messages = get_session_messages(session_id)
    user_message = {"role": "user", "content": user_message_text}
    messages.append(user_message)
    ai_message = get_new_ai_message(messages)
    messages.append(ai_message)
    save_session_messages(session_id, messages)
    return ai_message["content"]
