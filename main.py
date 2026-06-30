# to run project run this command streamlit run filename.py
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# ==========================
# Streamlit Configuration
# ==========================

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini AI Chatbot")

# ==========================
# Chat History
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# User Input
# ==========================

prompt = st.chat_input("Type your message...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history
    history = ""

    for msg in st.session_state.messages:
        history += f"{msg['role']}: {msg['content']}\n"

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history
    )

    answer = response.text

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)