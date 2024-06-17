import streamlit as st
import pandas as pd

def cargar_archivo():

    st.markdown("# :computer: Mi Aplicación Streamlit para Predecir El Abandono de Clientes")

    col_1, col_2, col_3 = st.columns(3, gap="large")
        
    with col_2:
        st.image(image="images/customer-rating.png", width=300)

    st.markdown(
                """
                ### ¡Bienvenido a la aplicación de predicción de abandono de clientes! 
                    
                Esta herramienta te ayudará a identificar a los clientes que tienen más probabilidades de abandonar tu negocio, lo que te permitirá tomar medidas preventivas y mejorar la retención de clientes.

                La aplicación utiliza un modelo de Machine Learning entrenado para analizar los patrones en los datos de tus clientes y predecir si abandonarán el servicio en un futuro próximo.

                "Para comenzar, sigue estos sencillos pasos:

                1. Sube tu conjunto de datos de clientes utilizando la opción "Subir" que se encuentra en la parte de abajo. Asegúrate de que tu archivo esté en formato CSV.
                2. Puedes dirigirte a la página de Análisis Exploratorio de Datos para analizar los datos que se cargaron.
                3. En la página de Preprocesamiento puedes eliminar columnas o valores vacíos y atípicos.
                4. Una vez realizado todo ese procedimiento puedes dirigirte a Entrenamiento para Entrenar tu modelo con los parámetros de cada modelo.
                5. Sube el modelo entrenado que utilizarás para realizar las predicciones. Asegúrate de que el modelo esté en formato PKL.
                6. Navega por las opciones en la barra lateral para ajustar los parámetros y personalizar tu análisis.
                7. Revisa las predicciones y las probabilidades generadas por el modelo.
                8. Descarga el informe con las predicciones y las probabilidades para cada cliente.

                ¡Buena suerte en tus esfuerzos para mejorar la retención de clientes y mantener a tus clientes satisfechos!
                """
            )

        
    st.markdown("### :open_file_folder: Sube el archivo que vas a entrenar")
    uploaded_file = st.file_uploader("Cargue su archivo CSV", type=["csv"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        #df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_file = uploaded_file
        st.session_state.df = pd.read_csv(uploaded_file)

        c1,c2,c3 = st.columns(3)
        with c2:
            st.image(image="images/servicio-al-cliente.png", width=250)

        st.markdown("### :chart_with_upwards_trend: ¿Deseas ver el dataset?, da clic aquí abajo")

        mostrar_dataset = st.radio("Escoge una opción", ["Mostrar Dataset", "Ocultar dataset"])
        if mostrar_dataset == "Mostrar Dataset":
            st.write(st.session_state.df)



        st.markdown("### :mag: ¿Deseas ver el head del dataset?, da clic aquí abajo")

        mostrar_head = st.checkbox("Mostrar head del dataset")
        if mostrar_head:
            st.write(st.session_state.df.head())
    
    elif "uploaded_file" in st.session_state:
        st.markdown('''
                    ## Acerca de los datos
                    ''')

        st.markdown(f"Archivo previamente subido: **{st.session_state.uploaded_file.name}**")
        st.markdown("### :chart_with_upwards_trend: ¿Deseas ver el dataset?, da clic aquí abajo")


        mostrar_dataset = st.radio("Escoge una opción", ["Mostrar Dataset", "Ocultar dataset"])
        if mostrar_dataset == "Mostrar Dataset":
            st.write(st.session_state.df)
        
        st.markdown("### :mag: ¿Deseas ver el head del dataset?, da clic aquí abajo")
        

        mostrar_head = st.checkbox("Mostrar head del dataset")
        if mostrar_head:
            st.write(st.session_state.df.head())

cargar_archivo()






