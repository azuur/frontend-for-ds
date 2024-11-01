from fastapi import Cookie, FastAPI, Form, Request, Response
import uuid
from fastapi import status

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from frontend_for_ds.backend import get_session_messages, reply

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    response: Response,
    session_id: str = Cookie(None),
):
    if session_id is None:
        # make uuid4 session_id and convert to str
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, path="/send")

    messages = get_session_messages(session_id)

    ui_messages = [
        {
            "sender": m["role"],
            "text": m["content"],
            "type": ("bot" if m["role"] == "assistant" else "user"),
        }
        for m in messages[1:]
    ]

    response = templates.TemplateResponse(
        "main.html", {"request": request, "messages": ui_messages}
    )
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.post("/send", response_class=HTMLResponse)
async def root(
    response: Response,
    user_input: str = Form(...),
    session_id: str = Cookie(None),
):
    if session_id is None:
        # make uuid4 session_id and convert to str
        session_id = str(uuid.uuid4())

    _ = reply(session_id, user_input)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.get("/reset")
async def reset_session(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response


def main() -> None:
    uvicorn.run(app)
