import streamlit as st
from escenario1 import escenario_1
from escenario2 import escenario_2
from escenario3 import escenario_3
from escenario4 import escenario_4



def prediccion():
    st.markdown("# :chart_with_upwards_trend: Predicción de Abandono de los Clientes")
    st.markdown("""
    En esta sección contarás con 4 escenarios para realizar predicciones distintas y conocer si los clientes abandonarán los servicios o no.  Nuestro modelo utiliza información demográfica y de uso del servicio para predecir la probabilidad de abandono.
    
    **Instrucciones:**
    
    - **Escenario 1:** Realiza predicciones manuales de los clientes que abandonarán a partir de un modelo pre-entrenado  que se encuentra cargado previamente
    - **Escenario 2:** Carga un conjunto de datos nuevo en la cual contenga todas las caracteristicas que se utilizaron en el "dataset_abandono" exceptuando la columna a predecir (abandono)
    - **Escenario 3:** Realiza la carga del modelo pre-entrenado (creado en la página de entrenamiento) en formato 'pkl' para realizar predicciones manuales de clientes que abandonarán.
    - **Escenario 4:** Realiza la carga de un dataset nuevo (sin la variable 'abandono') y de un modelo pre-entrenado para realizar la predicción de abandono de los clientes.
    """)
    st.divider()
    opciones = st.radio(
    "Seleccione un Escenario:",
    ["Escenario 1", "Escenario 2", "Escenario 3","Escenario 4"],horizontal=True)

    if opciones == 'Escenario 1':
        escenario_1()
    elif opciones == 'Escenario 2':
        escenario_2()
    elif opciones == 'Escenario 3':
        escenario_3()
    else:
        escenario_4()

prediccion()