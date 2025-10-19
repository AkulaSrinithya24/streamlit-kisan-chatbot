import streamlit as st
import requests

st.title("Kisan Suraksha AI Chatbot")

st.info("Supports English, Telugu, and Hindi queries. All backend NLP logic runs in the cloud.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Type your message", key="input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append(("You", user_input))
    try:
        resp = requests.post(
            "https://kisan-backend-production.up.railway.app/chat",  # <-- Your live Railway backend!
            json={"message": user_input},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            bot_reply = data.get("reply", "Sorry, no reply from backend.")
        else:
            bot_reply = f"Error: Backend returned status {resp.status_code}."
    except Exception as e:
        bot_reply = f"Connection error: {e}"

    st.session_state.chat_history.append(("Bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.success(f"**Bot:** {msg}")
