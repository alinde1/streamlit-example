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

min_score = 10/100
client = hfapi.Client(api_token=st.secrets['api_key'])
model = "mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"

st.header("Chatbot para refugiados")
st.caption(("Este es un bot de prueba y los textos son generados. ",
            "¡No consideres esta información como fiable! ",
            "Es preferible que consultes con tu especialista o asesor legal."))

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input("Tú: ","Hola, ¿cómo estás?", key="input")
    return input_text


user_input = get_text()

if user_input:

    max_score = 0
    max_answer = ""
    responses = []
    for _, _, files in os.walk("context"):
        for file in files:
            with open("context/" + file) as f:
                context = f.read()
                response = client.question_answering(user_input, context, model=model)
                if response.get('error'):
                    st.write(response['error'])
                else:
                    responses.append((response['answer'], response['score']))
                    if response['score'] > max_score:
                        max_score = response['score']
                        max_answer = response['answer']

    if max_score >= min_score:
        output = max_answer
    else:
        output = "Lo siento. No se la respuesta"

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
