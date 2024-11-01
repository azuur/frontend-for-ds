# minimally adapted from https://github.com/AnswerDotAI/fasthtml-example/blob/74d08b5c034f2ccca998353a34dbdad81276bfae/02_chatbot/README.md

import uuid
from fasthtml.common import (
    Script,
    Link,
    picolink,
    FastHTML,
    Div,
    Input,
    Form,
    Button,
    Group,
    Hidden,
    Titled,
    serve,
)
from fasthtml.core import cookie
from frontend_for_ds.backend import reply
from starlette.requests import Request

# Set up the app, including daisyui and tailwind for the chat component
hdrs = (
    picolink,
    Script(src="https://cdn.tailwindcss.com"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
    ),
)
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")


# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else "chat-bubble-secondary"
    chat_class = "chat-end" if user else "chat-start"
    return Div(cls=f"chat {chat_class}")(
        Div("user" if user else "assistant", cls="chat-header"),
        Div(msg, cls=f"chat-bubble {bubble_class}"),
        # Hidden(msg, name="messages"),
    )


def ChatInput():
    return Input(
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        cls="input input-bordered w-full",
        hx_swap_oob="true",
    )


@app.get
def index():
    page = Form(hx_post=send, hx_target="#chatlist", hx_swap="beforeend")(
        Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
        Div(cls="flex space-x-2 mt-2")(
            Group(ChatInput(), Button("Send", cls="btn btn-primary"))
        ),
    )
    return Titled("Chatbot Demo", page)


# Handle the form submission
@app.post
def send(msg: str, request: Request):

    session_id = request.cookies.get("session_id")
    if session_id is None:
        # make uuid4 session_id and convert to str
        session_id = str(uuid.uuid4())

    r = reply(session_id, msg)
    return (
        cookie("session_id", session_id),
        ChatMessage(msg, True),  # The user's message
        ChatMessage(r.rstrip(), False),  # The chatbot's response
        ChatInput(),
    )  # And clear the input field via an OOB swap


def main():
    serve()
