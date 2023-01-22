# Based on https://github.com/AI-Yash/st-chat/blob/main/examples/chatbot.py

import streamlit as st
from streamlit_chat import message
import requests
import simpletransformers
import pickle

st.set_page_config(
    page_title="Chatbot para refugiados",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Bearer API_TOKEN": st.secrets['api_key']}

st.header("Chatbot para refugiados")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def load_model():
    model_path = 'https://bitbucket.org/ml-learning/models/raw/9a5be506273ef6999ae4244653548c177cc748a0/models/model.pkl'
    r = requests.get(model_path, stream='True')
    if r.status_code == 200:
        model = pickle.load(r.raw)
        return model
    else:
        return None


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
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text


#model = load_model()
contexto_1 = """
Derecho a solicitar protección internacional.\n\n1. Las personas nacionales no comunitarias
y las apátridas presentes en territorio español tienen derecho a solicitar protección internacional en España.\n\n2.
Para su ejercicio, los solicitantes de protección internacional tendrán derecho a asistencia sanitaria y a asistencia
jurídica gratuita, que se extenderá a la formalización de la solicitud y a toda la tramitación del procedimiento,
y que se prestará en los términos previstos en la legislación española en esta materia, así como derecho a intérprete
en los términos del artículo 22 de la Ley Orgánica 4/2000.\n\nLa asistencia jurídica referida en el párrafo anterior
será preceptiva cuando las solicitudes se formalicen de acuerdo al procedimiento señalado en el artículo 21 de la
presente Ley.\n\n3. La presentación de la solicitud conllevará la valoración de las circunstancias determinantes
del reconocimiento de la condición de refugiado, así como de la concesión de la protección subsidiaria.
De este extremo se informará en debida forma al solicitante.\n\n4. Toda información relativa al procedimiento,
incluido el hecho de la presentación de la solicitud, tendrá carácter confidencial.
"""

user_input = get_text()

if user_input:
    # output = query({
    #     "inputs": {
    #         "past_user_inputs": st.session_state.past,
    #         "generated_responses": st.session_state.generated,
    #         "text": user_input,
    #     },"parameters": {"repetition_penalty": 1.33},
    # })
    output = "Working..." # prediction(contexto_1, user_input)[-1]

    # st.write(user_input)
    # st.write(output)
    # st.write(st.session_state)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output) #["generated_text"]

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
