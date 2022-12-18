import streamlit as st
import time

st.set_page_config(layout="wide")
st.title('Logging in Text Box')

def update_text():
    logtxt = text_input
    logtxtbox.text_area("Respuesta: ",logtxt, height = 500)

text_input = st.text_input("Pregunta", value="", on_change=update_text)

logtxtbox = st.empty()
logtxt = ""
logtxtbox.text_area("Respuesta: ",logtxt, height = 500)
