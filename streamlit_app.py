#  uri = st.secrets["URI"]
import streamlit as st
from google import genai

# --- Initialize Google GenAI client ---
# Make sure you set your GOOGLE_API_KEY in Streamlit secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Gemini Chat", page_icon="✨")

st.title("💬 Chat with Gemini (google-genai)")

# --- Store conversation in session state ---
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat input box ---
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.history.append({"role": "user", "text": user_input})

    # Stream AI response
    response_chunks = st.session_state.chat.send_message_stream(user_input)
    ai_response = ""
    response_placeholder = st.empty()

    for chunk in response_chunks:
        ai_response += chunk.text or ""
        response_placeholder.markdown(ai_response)

    # Save AI response
    st.session_state.history.append({"role": "model", "text": ai_response})

# --- Display chat history ---
for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["text"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["text"])
