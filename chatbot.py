# pip install langchain-openai streamlit
import streamlit as st
from langchain_openai import ChatOpenAI
import os


# Get OpenAI API key

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Set the environment variable OPENAI_API_KEY.")
    st.stop()


# Initialize LLM

llm = ChatOpenAI(
    api_key=openai_api_key,
    temperature=0.7,
    model="gpt-4o-mini"
)


# Chat history in Streamlit session state

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Streamlit UI

st.set_page_config(page_title="LLM Chatbot", page_icon="🤖")
st.title("LangChain Chatbot By DM")


# Send button
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="input_field")
    # Form submit button triggers on click OR Enter
    submitted = st.form_submit_button("Send")

if submitted  and user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate LLM response
    response = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})


# Display latest messages immediately

if st.session_state.chat_history:
    # Display last user + bot messages
    for msg in st.session_state.chat_history[-2:]:
        role = "You" if msg["role"] == "user" else "Bot"
        st.markdown(f"**{role}:** {msg['content']}")


# Optional: Show full chat history

if st.checkbox("Show Chat History"):
    st.markdown("---")
    for msg in st.session_state.chat_history:
        role = "You" if msg["role"] == "user" else "Bot"
        st.markdown(f"**{role}:** {msg['content']}")
