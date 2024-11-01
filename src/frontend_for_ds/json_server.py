from typing import Annotated
from fastapi import FastAPI, Header
import uuid

import uvicorn

from frontend_for_ds.backend import reply

app = FastAPI()


@app.post("/")
async def root(
    user_message_text: str,
    session_id: Annotated[str | None, Header()] = None,
):
    if session_id is None:
        # make uuid4 session_id and convert to str
        session_id = str(uuid.uuid4())

    response = reply(session_id, user_message_text)

    return {"session_id": session_id, "response": response}


def main() -> None:
    uvicorn.run(app)
