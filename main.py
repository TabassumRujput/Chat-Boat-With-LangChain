import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


st.set_page_config(
    page_title='Chat with Gemimi',
    page_icon=":brain:",
    layout="centered",
)
genai.configure(api_key=os.environ["google_api_key"])
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

def translate_role_for_streamlit(user_role):
    if user_role== "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []



# Display the chatbot's title on the page
st.title("✨ Gemini - ChatBot")
context_str=""
# Display the chat history
for message in st.session_state.chat_session:
    context_str+=message["content"]
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini... ")
if user_prompt:
    new_prompt=user_prompt+context_str
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_session.append({"role":"user","content":user_prompt})


    # Send user's message to Gemini-Pro and get the response
    gemini_response =chat.send_message(new_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    st.session_state.chat_session.append({"role": "assistant", "content": gemini_response.text})




