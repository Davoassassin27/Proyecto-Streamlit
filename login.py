import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
from app import app

st.set_page_config(page_title="App de Predicción",
                   page_icon='images/customer-rating.png',
                   layout='wide', 
                   initial_sidebar_state='expanded')

def login():
    # Hashing
    passwords_to_hash = ['12345', 'abcdef']
    hashed_paswords = Hasher(passwords_to_hash).generate()

    #st.write(hashed_paswords)
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    col1, col2,col3 = st.columns(3)

    with col2:
        authenticator.login()
    
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Bienvenido a la aplicación:  **{st.session_state["name"]}**')
        app()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        col4, col5, col6 = st.columns(3)
        with col5:
            st.warning('Por favor, ingrese sus credenciales correctamente')
login()