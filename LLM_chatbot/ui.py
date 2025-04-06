import streamlit as st
import requests
import base64
import uuid

def get_base64_image_from_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()

icon_url = "https://img.freepik.com/premium-vector/chatbot-concept-background-realistic-style_730620-44319.jpg"
chatbot_icon_b64 = get_base64_image_from_url(icon_url)

st.set_page_config(
    page_title="LLAMA2 Chatbot",
    page_icon=f"data:image/jpeg;base64,{chatbot_icon_b64}",
    layout="centered"
)

theme = st.sidebar.radio("🌗 Choose Mode", ["Night Swift", "Light Swift"])

background_dark = "https://wallpaperaccess.com/full/8691990.png"
background_light = "https://images.unsplash.com/photo-1603791440384-56cd371ee9a7"
background = background_dark if theme == "Night Swift" else background_light
font_color = "white" if theme == "Night Swift" else "black"
container_bg = "rgba(0,0,0,0.4)" if theme == "Night Swift" else "rgba(255,255,255,0.6)"

extra_style = """
<style>
    header, .st-emotion-cache-1dp5vir, .st-emotion-cache-1avcm0n {
        color: black !important;
    }
    .st-emotion-cache-18ni7ap {
        background-color: transparent !important;
    }
    label, .stTextInput label {
        color: black !important;
        font-weight: bold;
    }
</style>
""" if theme == "Light Swift" else ""

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{background}");
        background-size: cover;
        background-position: center;
        color: {font_color};
    }}
    .block-container {{
        background-color: {container_bg};
        border-radius: 1rem;
        padding: 2rem;
    }}
    </style>
    {extra_style}
""", unsafe_allow_html=True)

st.title("🦙 LLaMA2 Chatbot")
st.markdown("Ask me anything related to orders, pricing, tech support, and more!")

API_URL = "http://localhost:8000/chat"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

user_input = st.text_input("💬 Your Message", key="input_text")

if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        res = requests.post(API_URL, json={"session_id": st.session_state.session_id, "prompt": user_input})
        bot_reply = res.json()["response"]
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))

if st.session_state.chat_history:
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")

st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.input_text = ""