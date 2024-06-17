import streamlit as st
from inicio import cargar_archivo
from eda import eda
from entrenamiento import entrenamiento
from preprocesamiento import preprocesamiento
from prediccion import prediccion
from reporte import reporte
from extra_features import extra_features

st.set_page_config(page_title="App de Predicción",
                   page_icon='images/customer-rating.png',
                   layout='wide', 
                   initial_sidebar_state='expanded')

def hide_elements():
    configuracion="""
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """
    st.markdown(configuracion,unsafe_allow_html=True)

def app():
    hide_elements()

    nombresPaginas = {
        "Inicio": cargar_archivo,
        "Análisis Exploratorio de Datos": eda,
        "Preprocesamiento de Datos":preprocesamiento,
        "Entrenamiento y Prueba": entrenamiento,
        "Predicción": prediccion,
        "Reporte": reporte,
        "Funciones Extra": extra_features
    }

    nombres_Paginas = st.sidebar.selectbox("Escoja una página", nombresPaginas.keys())
    st.sidebar.divider()
    nombresPaginas[nombres_Paginas]()


app()