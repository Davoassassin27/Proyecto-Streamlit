import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from io import BytesIO

def escenario_3():
    st.markdown("### Suba el modelo pre-entrenado")
    modelo_entrenado = st.file_uploader("Suba el Modelo Entrenado", type=["pkl"])
    if modelo_entrenado is not None:
        carga_modelo = pickle.load(modelo_entrenado)

        column = ["Genero","PersonaMayor", "Socio", "Dependientes", "Permanencia", "ServicioTelefonico", "VariasLineas", "ServicioInternet",
                "SeguridadLinea", "CopiaSeguridadLinea", "ProteccionDispositivo", "ServicioTecnico", "ServicioTV", "ServicioPeliculas",
                "Contrato", "FacturacionElectronica", "MetodoPago", "RecargoMensual", "TotalRecargo"]
        datos_dicc = {}
        if "Genero" in column:
            genero = st.sidebar.selectbox('Genero', ("Femenino", "Masculino"), key='genero_selectbox')
            datos_dicc['Genero'] = genero

        if "PersonaMayor" in column:
            PersonaMayor = st.sidebar.selectbox('¿Es Una Persona Adulta Mayor?(Si =1,No=0)', (0, 1), key='PersonaMayor_selectbox_1')
            datos_dicc["PersonaMayor"] = PersonaMayor

        if "Socio" in column:
            Socio = st.sidebar.selectbox('¿Eres socio?', ("Si", "No"), key='socio_selectbox')
            datos_dicc["Socio"] = Socio

        if "Dependientes" in column:
            Dependientes = st.sidebar.selectbox('¿Eres Dependiente?', ("Si", "No"), key='dependientes_selectbox')
            datos_dicc["Dependientes"] = Dependientes

        if "Permanencia" in column:
            Permanencia = st.sidebar.slider('¿Cuantos Meses tienes de Contrato?', 0, 72, 29, key='permanencia_slider')
            datos_dicc["Permanencia"] = Permanencia

        if "ServicioTelefonico" in column:
            ServicioTelefonico = st.sidebar.selectbox('¿Tienes Servicio Telefónico?', ("Si", "No"), key='servicioTelefonico_selectbox')
            datos_dicc["ServicioTelefonico"] = ServicioTelefonico

        if "VariasLineas" in column:
            VariasLineas = st.sidebar.selectbox('¿Tiene Múlitples Líneas?', ("Si", "No", "Sin Servicio Telefónico"), key='variasLineas_selectbox')
            datos_dicc["VariasLineas"] = VariasLineas

        if "ServicioInternet" in column:
            ServicioInternet = st.sidebar.selectbox('¿Que tipo de servicio de Internet Tiene?', ("DLS", "No", "Fibra Óptica"), key='servicioInternet_selectbox')
            datos_dicc["ServicioInternet"] = ServicioInternet

        if "SeguridadLinea" in column:
            SeguridadLinea = st.sidebar.selectbox('¿Tiene Seguridad En Línea?', ("Si", "No", "Sin Servicio de Internet"), key='seguridadLinea_selectbox')
            datos_dicc["SeguridadLinea"] = SeguridadLinea

        if "CopiaSeguridadLinea" in column:
            CopiaSeguridadLinea = st.sidebar.selectbox('Tiene Copia de Seguridad en Línea ?', ("Si", "No", "Sin Servicio de Internet"), key='copiaSeguridadLinea_selectbox')
            datos_dicc["CopiaSeguridadLinea"] = CopiaSeguridadLinea

        if "ProteccionDispositivo" in column:
            ProteccionDispositivo = st.sidebar.selectbox('¿Tiene Protección del Dispositivo?', ("Si", "No", "Sin Servicio de Internet"), key='proteccionDispositivo_selectbox')
            datos_dicc["ProteccionDispositivo"] = ProteccionDispositivo

        if "ServicioTecnico" in column:
            ServicioTecnico = st.sidebar.selectbox('¿Tiene Soporte Técnico?', ("Si", "No", "Sin Servicio de Internet"), key='servicioTecnico_selectbox')
            datos_dicc["ServicioTecnico"] = ServicioTecnico

        if "ServicioTV" in column:
            ServicioTV = st.sidebar.selectbox('¿Tiene Servicio de TV?', ("Si", "No", "Sin Servicio de Internet"), key='servicioTV_selectbox')
            datos_dicc["ServicioTV"] = ServicioTV

        if "ServicioPeliculas" in column:
            ServicioPeliculas = st.sidebar.selectbox('¿Tiene Servicio de Películas?', ("Si", "No", "Sin Servicio de Internet"), key='servicioPeliculas_selectbox')
            datos_dicc["ServicioPeliculas"] = ServicioPeliculas

        if "Contrato" in column:
            Contrato = st.sidebar.selectbox('Tipo de Contrato del Cliente', ("Mensual", "un anio", "dos anios"), key='contrato_selectbox')
            datos_dicc["Contrato"] = Contrato

        if "FacturacionElectronica" in column:
            FacturacionElectronica = st.sidebar.selectbox('¿Recibe Factura Electrónica?', ("Si", "No"), key='facturacionElectronica_selectbox')
            datos_dicc["FacturacionElectronica"] = FacturacionElectronica

        if "MetodoPago" in column:
            MetodoPago = st.sidebar.selectbox('¿Cuál es el Metodo de Pago?', ("Cheque Electrónico", "Cheque por Correo", "Transferencia bancaria (automática)", "Tarjeta de crédito (automática)"), key='metodoPago_selectbox')
            datos_dicc["MetodoPago"] = MetodoPago

        if "RecargoMensual" in column:
            RecargoMensual = st.sidebar.number_input('Recargo Mensual', 0.00, 200.00, 70.35, key='recargoMensual_number_input')
            datos_dicc["RecargoMensual"] = RecargoMensual

        if "TotalRecargo" in column:
            TotalRecargo = st.sidebar.number_input('Recargo Anual', 0.00, 10000.00, 1000.00, key='totalRecargo_number_input')
            datos_dicc["TotalRecargo"] = TotalRecargo

        dataset_nuevo = pd.DataFrame(datos_dicc, index=[0])
        st.write('Actualmente usando parámetros de entrada (que se muestran a continuación):')
        st.write(dataset_nuevo)




        for i in dataset_nuevo.select_dtypes(include='object').columns:
            dataset_nuevo[i] = LabelEncoder().fit_transform(dataset_nuevo[i])
            scaler = StandardScaler().fit(dataset_nuevo[["TotalRecargo"]])
            dataset_nuevo["TotalRecargo"] = scaler.transform(dataset_nuevo[["TotalRecargo"]])
            scaler = StandardScaler().fit(dataset_nuevo[["RecargoMensual"]])
            dataset_nuevo["RecargoMensual"] = scaler.transform(dataset_nuevo[["RecargoMensual"]])

        prediccion_modelo = carga_modelo.predict(dataset_nuevo)
        prediction_proba_modelo = carga_modelo.predict_proba(dataset_nuevo)

        col_nada_predi, col_nada_pro = st.columns((5, 5))
        
        with col_nada_predi:
            st.subheader('Predicción')
            df_abandono = pd.DataFrame(prediccion_modelo, columns=["Abandono"])
            df_abandono = df_abandono.applymap(lambda x: "No" if x == 0 else "Si")
            st.write(df_abandono)
        with col_nada_pro:
            st.subheader('Probabilidad de predicción')
            df_abandono = pd.DataFrame(prediction_proba_modelo.argmax(axis=1), columns=["Abandono"])
            df_abandono = df_abandono.applymap(lambda x: "No" if x == 0 else "Si")
            probabilidades = np.where(df_abandono["Abandono"] == "No", prediction_proba_modelo[:, 0], prediction_proba_modelo[:, 1])
            df_resultado = pd.DataFrame({"Abandono": df_abandono["Abandono"], "Probabilidad": probabilidades})
            st.write(df_resultado)
        for index, row in df_resultado.iterrows():
            abandono = row.iloc[0]
            probabilidad = row.iloc[1] * 100
            if abandono == "Si":
                st.markdown(f"### La persona tiene una probabilidad del {probabilidad:.2f}% de que abandone los servicios.")
            else:
                st.markdown(f"### La persona tiene una probabilidad del {probabilidad:.2f}% de que NO abandone los servicios.")

escenario_3()