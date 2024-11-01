from .json_server import main as json_server_main
from .streamlit_server import main as streamlit_server_main
from .plain_demo import main as plain_demo_main
from .html_server import main as html_server_main
from .fasthtml_server import main as fasthtml_server_main

# from .dash_server import main as dash_server_main

__all__ = [
    "json_server_main",
    "streamlit_server_main",
    "plain_demo_main",
    "html_server_main",
    "fasthtml_server_main",
    # "dash_server_main",
]
