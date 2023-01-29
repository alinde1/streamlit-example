# Based on https://github.com/AI-Yash/st-chat/blob/main/examples/chatbot.py

import streamlit as st
from streamlit_chat import message
import requests
import pickle
import hfapi
import os

st.set_page_config(
    page_title="Chatbot para refugiados",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Bearer API_TOKEN": st.secrets['api_key']}

client = hfapi.Client(api_token=st.secrets['api_key'])
model = "mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"

st.header("Chatbot para refugiados")
st.caption("Este es un bot de prueba y los textos son generados. ¡No consideres esta información como fiable! Es preferible que consultes con tu especialista o asesor legal.")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


# def prediction(context, question, limit=5):
#   to_predict = [
#       {
#           "context": context,
#           "qas": [
#               {
#                   "question": question,
#                   "id": "0",
#               }
#           ],
#       }
#   ]
#   answers, probabilities = model.predict(to_predict)
#   answers = answers[0]["answer"][:limit]
#   return answers


def query(payload):
    st.write(payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_text():
    input_text = st.text_input("Tú: ","Hola, ¿cómo estás?", key="input")
    return input_text


context = ""
for _, _, files in os.walk("context"):
    for file in files:
        with open("context/" + file) as f:
            data = f.read()
            context = "\n".join([context, data])

user_input = get_text()

if user_input:
    response = client.question_answering(user_input, context, model=model)
    output = response['answer'] # "Lo siento. No tengo cargado ningún modelo para poder contestarte"

    # st.write(user_input)
    # st.write(output)
    # st.write(st.session_state)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output) #["generated_text"]

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
