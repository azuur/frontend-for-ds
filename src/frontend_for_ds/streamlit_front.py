# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app

import streamlit as st

from frontend_for_ds.backend import get_session_messages, reply


def _get_session():
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session


def display_messages(messages: list[dict[str, str]]):
    for message in messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def streamlit_render():

    session_id = _get_session().id
    messages = get_session_messages(session_id)
    display_messages(messages)

    st.title("AI assistant demo!")

    if user_message_text := st.chat_input("..."):

        ai_message_text = reply(session_id, user_message_text)
        with st.chat_message("user"):
            st.markdown(user_message_text)

        with st.chat_message("assistant"):
            st.markdown(ai_message_text)


if __name__ == "__main__":
    streamlit_render()
