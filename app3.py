# app3.py
import streamlit as st
from groq import Groq

# Load the API key securely from Streamlit Cloud secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Your niche assistant behavior
SYSTEM_PROMPT = (
    "You are a warm, helpful, and friendly custom chatbot "
    "Explain topics clearly, avoid scary language. "
    "Keep it under 130 words."
)

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Niche Chatbot", page_icon="💬")
st.title("Custom Chatbot")
st.caption("Developed by Kirill.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Show previous messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Handle user input
user_input = st.chat_input("Ask your question here...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ Error: {e}")
