import streamlit as st
from google import genai
import time

# --- Page Config ---
st.set_page_config(page_title="Gemini Chat", page_icon="✨", layout="wide")

# --- Custom CSS for Modern UI ---
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
    }
    .chat-bubble {
        padding: 1rem 1.2rem;
        border-radius: 1.2rem;
        margin: 0.5rem 0;
        max-width: 75%;
        word-wrap: break-word;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        animation: fadeIn 0.3s ease-in-out;
    }
    .user-bubble {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.4rem;
    }
    .ai-bubble {
        background: white;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 0.4rem;
    }
    .chat-row {
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }
    .avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .typing {
        display: inline-block;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Google GenAI Client ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- Title ---
st.markdown("<h1 class='main-title'>💬 Chat with Gemini</h1>", unsafe_allow_html=True)

# --- Session State ---
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat Input ---
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
        response_placeholder.markdown(
            f"""
            <div class='chat-row'>
                <img src="https://i.imgur.com/8Km9tLL.png" class="avatar">
                <div class='chat-bubble ai-bubble'>{ai_response}<span class="typing">▌</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.03)

    response_placeholder.markdown(
        f"""
        <div class='chat-row'>
            <img src="https://i.imgur.com/8Km9tLL.png" class="avatar">
            <div class='chat-bubble ai-bubble'>{ai_response}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Save AI response
    st.session_state.history.append({"role": "model", "text": ai_response})

# --- Display History ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class='chat-row' style="justify-content:flex-end;">
                <div class='chat-bubble user-bubble'>{msg['text']}</div>
                <img src="https://i.imgur.com/BrXcYMR.png" class="avatar">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class='chat-row'>
                <img src="https://i.imgur.com/8Km9tLL.png" class="avatar">
                <div class='chat-bubble ai-bubble'>{msg['text']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)
