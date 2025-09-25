import streamlit as st
from google import genai
import time

# --- Page Config ---
st.set_page_config(page_title="Gemini Chat", page_icon="✨", layout="wide")

# --- Custom CSS for beautiful UI ---
st.markdown("""
<style>
    .chat-bubble {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 1rem;
        line-height: 1.4;
    }
    .user-bubble {
        background-color: #DCF8C6;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 0.2rem;
    }
    .ai-bubble {
        background-color: #F1F0F0;
        margin-left: 0;
        margin-right: auto;
        border-bottom-left-radius: 0.2rem;
    }
    .chat-avatar {
        height: 40px;
        width: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .chat-row {
        display: flex;
        align-items: flex-start;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Google GenAI client ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("💬 Gemini AI — Your Smart Companion")

# --- Session State ---
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

# --- Input Box ---
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
        # typing animation effect
        response_placeholder.markdown(
            f"<div class='chat-bubble ai-bubble'>{ai_response}▌</div>", 
            unsafe_allow_html=True
        )
        time.sleep(0.03)

    response_placeholder.markdown(
        f"<div class='chat-bubble ai-bubble'>{ai_response}</div>", 
        unsafe_allow_html=True
    )

    # Save AI response
    st.session_state.history.append({"role": "model", "text": ai_response})

# --- Display Chat History ---
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble user-bubble'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble ai-bubble'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
