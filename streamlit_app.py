# Based on https://github.com/AI-Yash/st-chat/blob/main/examples/chatbot.py

import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="Chatbot para refugiados",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Bearer API_TOKEN": st.secrets['api_key']}

st.header("Chatbot para refugiados")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def query(payload):
    st.write(payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if user_input:
    # output = query({
    #     "inputs": {
    #         "past_user_inputs": st.session_state.past,
    #         "generated_responses": st.session_state.generated,
    #         "text": user_input,
    #     },"parameters": {"repetition_penalty": 1.33},
    # })
    output = "Probando..."

    # st.write(user_input)
    # st.write(output)
    # st.write(st.session_state)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output) #["generated_text"]

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
