import streamlit as st
import time
import numpy as np
import pandas as pd
import pydeck as pdk

def extra_features():

    tabs = ["Multimedia", "Funciones Extra con Datos", "Componentes Estéticos", "Chat Elements"]
    tab = st.tabs(tabs)

    def stream_data():
        texto = """
        Hola, en esta pagina verás algunas funcionalidades extra que 
        se pueden hacer con streamlit para que luego puedas elegir lo que realmente necesites. 
        Espero disfrutes estas funcionalidades!
        """
        for palabra in texto.split(" "):
            yield palabra + " "
            time.sleep(0.02)

        yield pd.DataFrame(
            np.random.randn(5, 10),
            columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        )

    with tab[0]:
        st.write("Estos son algunos de las funcionalidades multimedia en streamlit:")
        
        st.markdown("## Generar texto de forma dinámica")
        
        if st.button("¡Presiona aquí!"):
            st.write_stream(stream_data)
    
        st.divider()
    
        st.markdown("## Elemento para capturar cámara")
        
        captura = st.camera_input("Tomate una foto aquí" )
        
        if captura is not None:
            st.image(captura)

        st.divider()
        
        st.markdown("## Elemento para subir archivos")
        
        foto_subida = st.file_uploader("Sube una foto o video aquí", type=["jpg", "jpeg", "png", "mp4", "mov"])
        
        if foto_subida is not None:

            with st.spinner('Espera'):
                time.sleep(5)
            st.success("El archivo se cargó correctamente!")
            st.balloons()
        else:
            st.warning("Sube un archivo para continuar.")

        st.divider()

        st.markdown("## Elemento para subir videos")
        
        video_subido = st.file_uploader("Sube un video aquí", type=["mp4", "mov"])
        if video_subido is not None:
            st.video(video_subido)
            with st.spinner('Espera'):
                time.sleep(5)
            st.success("El video se cargó correctamente!")
        else:
            st.warning("Sube un video para continuar.")

        st.divider()
        
        st.markdown("## Elemento para subir audios")
        audio_subido = st.file_uploader("Sube un audio aquí", type=["mp3", "wav"])
        if audio_subido is not None:
            st.audio(audio_subido)
            with st.spinner('Espera'):
                time.sleep(5)
            st.success("El audio se cargó correctamente!")
        else:
            st.warning("Sube un audio para continuar.")


    with tab[1]:
        st.write("Funciones Extra con Datos:")
        
        dataset = st.file_uploader("Sube tu dataset aquí", type=["csv"])
        
        if dataset is not None:
            st.success("El dataset se cargó correctamente!")
            with st.spinner('Cargando dataset...'):
                df = pd.read_csv(dataset)
                st.data_editor(df)
                st.success("Dataset cargado y editable!")

    
            st.divider()
                
            st.markdown("## Elemento para seleccionar color")
            st.write("Selecciona un color :")
            color = st.color_picker("Elige un color", "#00f900")
            st.markdown(f"<h1 style='color: {color};'>Texto con color personalizado</h1>", unsafe_allow_html=True)

            st.divider()
        
            st.write("Gráfico de mapa con pydeck:")
                
            layer = pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position=["lon", "lat"],
                auto_highlight=True,
                elevation_scale=50,
                pickable=True,
                elevation_range=[0, 3000],
                extruded=True,
                coverage=10
                )
                
                
            view_state = pdk.ViewState(
                longitude=-102.5528,
                latitude=23.6345,
                zoom=6,
                min_zoom=5,
                max_zoom=15,
                pitch=40.5,
                bearing=-27.36,
            )

            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "{position}\nCount: {elevationValue}"}
            )
                
            mostrar_grafico = st.checkbox("Mostrar gráfico de pydeck")
            if mostrar_grafico:

                st.pydeck_chart(r) 


                st.info("Gráfico de pydeck mostrado")

            st.divider()
                
            with st.expander("Código del gráfico en pydeck"):
                st.code("""
                    import pydeck as pdk

                    layer = pdk.Layer(
                        "HexagonLayer",
                        data=df,
                        get_position=["lon", "lat"],
                        radius=200,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    
                    )
                    view_state = pdk.ViewState(
                        latitude=df["lat"].mean(),
                        longitude=df["lon"].mean(),
                        zoom=5,
                        pitch=50,
                    )
                    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{position}\nCount: {elevationValue}"})
                    st.pydeck_chart(r)
                    """)
                
            st.divider()

                
            df_ficticio = pd.DataFrame(
                np.random.randn(100, 3),
                columns=["Ventas", "Costo", "Presupuesto"],
                index=pd.date_range("2022-01-01", periods=100)
            )
                
            st.write("Dataframe:")
            st.dataframe(df_ficticio)
                
            st.write("Filtrar datos con date y time picker:")
            start_date = pd.to_datetime(st.date_input("Start date", pd.to_datetime("2022-01-01")))
            end_date = pd.to_datetime(st.date_input("End date", pd.to_datetime("2022-12-31")))
                
            filtered_df = df_ficticio[(df_ficticio.index >= start_date) & (df_ficticio.index <= end_date)]

            st.dataframe(filtered_df)


    with tab[2]:
        st.toast("Ejemplo de Toast", icon="✅")
        
        st.write("Componentes Esteticos:")
        st.write("Este es un popover", help="Este es un popover con descripción")

        st.divider()
        
        with st.container():
            st.write("Ejemplo de sección con container:")
            if st.button("Activar Snow"):

                st.snow()
            if st.button("Activar Balloons"):
                st.balloons()

            with st.popover("Abre aqui!"):
                st.markdown("Hola! 👋")

                name = st.text_input("¿Cual es tu nombre?")
                st.write("Nombre:", name)
        
        
        st.divider()
        
        text_area = st.text_area("Ingresa texto aquí")
        if text_area:
            st.success("Texto ingresado!")
        else:
            st.error("No se ha ingresado texto.")
        
    with tab[3]:
        prendido = st.toggle("¿Quieres un poco de matemática?")
        if prendido:
            st.latex(r'''
                        a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
                        \sum_{k=0}^{n-1} ar^k =
                        a \left(\frac{1-r^{n}}{1-r}\right)
                    ''')

extra_features()