import streamlit as st
import requests

CHAT_URL = "http://127.0.0.1:5000/api/chat/"


def render_chatbot():
    st.header("AI Chat")

    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask a question")

    if st.button("Send") and user_input:
        payload = {
            "question": user_input
        }

        if st.session_state.session_id:
            payload["session_id"] = st.session_state.session_id

        response = requests.post(CHAT_URL, json=payload)

        if response.status_code == 200:
            data = response.json()

            st.session_state.session_id = data["session_id"]

            st.session_state.chat_history.append(
                ("user", user_input)
            )
            st.session_state.chat_history.append(
                ("assistant", data["answer"])
            )

        else:
            st.error("Chat failed")

    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Assistant:** {message}")
