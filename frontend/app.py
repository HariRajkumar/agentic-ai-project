import streamlit as st
from components.uploader import render_uploader
from components.chatbot import render_chatbot

st.set_page_config(
    page_title="Agentic AI Assistant",
    layout="wide"
)

st.title("Agentic AI Document Assistant")

# Sidebar Chat
with st.sidebar:
    render_chatbot()

# Main upload + summary area
render_uploader()
