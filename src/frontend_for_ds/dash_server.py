# Adapted from https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-gpt3-chatbot/app.py

from pathlib import Path
import uuid
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from frontend_for_ds.backend import get_session_messages, reply


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    # logo = html.Img(
    #     src=app.get_asset_url("dash-logo.png"),
    #     style={"float": "right", "height": 60},
    # )
    return dbc.Row([dbc.Col(title, md=8)])


def textbox(text, box="AI", name="AI"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(
            text, style=style, body=True, color="primary", inverse=True
        )

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("ai.jpeg"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(
            text, style=style, body=True, color="light", inverse=False
        )

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")


# Define app
assets_path = Path(__file__).parent.parent.parent / "static"
app = dash.Dash(
    __name__,
    assets_folder=assets_path,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server


# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(
            id="user-input", placeholder="Write to the chatbot...", type="text"
        ),
        dbc.Button("Submit", id="submit"),
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Dash GPT Chatbot", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=[]),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
        dcc.Store(id="session-id", data=None),
    ],
)


@app.callback(
    Output("display-conversation", "children"),
    [Input("store-conversation", "data")],
)
def update_display(chat_history):
    return [
        (
            textbox(message["content"], box="user")
            if message["role"] == "user"
            else textbox(message["content"], box="AI")
        )
        for message in chat_history[1:]
    ]


@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@app.callback(
    [
        Output("store-conversation", "data"),
        Output("loading-component", "children"),
        Output("session-id", "data"),
    ],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [
        State("user-input", "value"),
        State("store-conversation", "data"),
        State("session-id", "data"),
    ],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history, session_id):

    if session_id is None:
        session_id = str(uuid.uuid4())

    if n_clicks == 0 and n_submit is None:
        return [], None, session_id

    if user_input is None or user_input == "":
        return chat_history, None, session_id

    _ = reply(session_id, user_input)
    chat_history = get_session_messages(session_id)

    return chat_history, None, session_id


def main():
    app.run_server(debug=True)
