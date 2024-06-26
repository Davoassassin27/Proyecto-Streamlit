import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, accuracy_score
import plotly.graph_objs as go
import pandas as pd
import pickle
import plotly.figure_factory as ff


def input_entrenamiento(val1, val2):
    if val1 + val2 < 100:
        diff = 100 - (val1 + val2)
        val2 += diff
    return val1, val2

def convert_model_to_bytes(model):
    model_bytes = pickle.dumps(model)
    return model_bytes



# if "data" not in st.session_state:
#     st.session_state.data = pd.read_csv('datasets/datos_preprocesados.csv')


def entrenamiento():
    st.markdown("# :bar_chart: Entrenamiento de Datos")

    # if "preprocessing_done" not in st.session_state:
    #     st.session_state.preprocessing_done = False

    # Verificar si los datos han sido cargados en session_state
    if "data" not in st.session_state:
        st.image("images/upload-cloud-data.png", width=300)
        st.write("Debe ingresar el dataset primero. Diríjase a la página principal.")
    
    else:
        if "data_entre" not in st.session_state:
            st.session_state.data_entre = st.session_state.predf.copy()
        data = st.session_state.data_entre
    

        # Parámetros para entrenar el modelo
        st.markdown("### Parámetros para Entrenar el Modelo")

        modelo = st.sidebar.selectbox("Escoja el modelo:", ("Clasificador de Regresión Logística",
                                                            "Clasificador K-vecinos más Cercanos",
                                                            "Clasificador de Árboles de Decisión",
                                                            "Clasificador de Bosque Aleatorio"))
        randomstate = st.sidebar.number_input("Ingrese el Random_State", min_value=0, max_value=10000, value=0)
        train_perc = st.sidebar.slider("Porcentaje de entrenamiento:", min_value=0, max_value=100, value=80)
        test_perc = 100 - train_perc

        st.sidebar.divider()


        st.sidebar.markdown(f"### Parámetros de {modelo}")
        
        # Modelo: Regresión Logistica

        if modelo == "Clasificador de Regresión Logística":
            solver = st.sidebar.selectbox("Solver", ('lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga'))
            penalty = st.sidebar.selectbox("Penalty", ("l2", "l1", "elasticnet", None))

            # Validación de combinaciones válidas de solver y penalty
            if solver in ['lbfgs', 'newton-cg', 'sag'] and penalty not in ['l2', None]:
                st.warning(f"El solver '{solver}' solo soporta las penalizaciones 'l2' o 'none'. Se establecerá 'l2' por defecto.")
                penalty = 'l2'
            elif solver == 'liblinear' and penalty not in ['l1', 'l2']:
                st.warning(f"El solver 'liblinear' solo soporta las penalizaciones 'l1' o 'l2'. Se establecerá 'l2' por defecto.")
                penalty = 'l2'
            elif solver == 'saga' and penalty not in ['elasticnet', 'l1', 'l2', None]:
                st.warning(f"El solver 'saga' solo soporta las penalizaciones 'elasticnet', 'l1', 'l2', o 'none'. Se establecerá 'l2' por defecto.")
                penalty = 'l2'

            C = st.sidebar.number_input("C", min_value=0.01, max_value=100.00, value=1.0)
            fit_intercept = st.sidebar.selectbox("Fit intercept", ("True", "False"))
            fit_intercept = True if fit_intercept == "True" else False

            modelo_entrenar = LogisticRegression(penalty=penalty, C=C, fit_intercept=fit_intercept, solver=solver)
            parametros = {"penalty": penalty, "C": C, "fit_intercept": fit_intercept, "solver": solver}

        # Modelo: KNN

        elif modelo == "Clasificador K-vecinos más Cercanos":
            n_neighbors = st.sidebar.number_input("N neighbors", min_value=0, max_value=50, value=5)
            weights = st.sidebar.selectbox("Weights", ("uniform", "distance"))
            algorithm = st.sidebar.selectbox("Algorithm", ("auto", "ball_tree", "kd_tree", "brute"))
            p = st.sidebar.selectbox("p", (2, 1))

            modelo_entrenar = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, algorithm=algorithm, p=p)
            parametros = {"n_neighbors": n_neighbors, "weights": weights, "algorithm": algorithm, "p": p}

        # Modelo: Árbol de Decisión

        elif modelo == "Clasificador de Árboles de Decisión":
            criterion = st.sidebar.selectbox("criterion", ("gini", "entropy", "log_loss"))
            splitter = st.sidebar.selectbox("splitter", ("best", "random"))
            max_depth = st.sidebar.selectbox("max_depth", (None, "Numeros"))
            if max_depth == "Numeros":
                max_depth = st.sidebar.slider("max_depth", 1, 100, 1)
            else:
                max_depth = None
            min_samples_split = st.sidebar.slider("min_samples_split", 1, 50, 2)

            modelo_entrenar = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split)
            parametros = {"criterion": criterion, "splitter": splitter, "max_depth": max_depth, "min_samples_split": min_samples_split}

        # Modelo: Árbol Aleatorio

        elif modelo == "Clasificador de Bosque Aleatorio":
            n_estimators = st.sidebar.slider("n_estimators", 10, 200, 100)
            criterion = st.sidebar.selectbox("criterion", ("gini", "entropy", "log_loss"))
            max_depth = st.sidebar.selectbox("max_depth", (None, "Numeros"))
            if max_depth == "Numeros":
                max_depth = st.sidebar.slider("max_depth", 1, 100, 1)
            else:
                max_depth = None
            min_samples_split = st.sidebar.slider("min_samples_split", 1, 50, 2)

            modelo_entrenar = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split)
            parametros = {"n_estimators": n_estimators, "criterion": criterion, "max_depth": max_depth, "min_samples_split": min_samples_split}

        # Visualización de Parametros

        datos = {
            'Variable Dependiente': "Abandono",
            'Modelo': modelo,
            'Entrenamiento': f"{train_perc}%",
            'Prueba': f"{test_perc}%",
            "Random_State": randomstate
        }
        entre = pd.DataFrame(datos, index=[0])
        st.write(entre)
        st.markdown(f"### Parámetros del modelo {modelo}")
        para = pd.DataFrame(parametros, index=[0])
        st.write(para)

        # Botón de Entrenamiento

        boton_entrenar = st.button("Entrenar el modelo")
        if boton_entrenar:
            model = entrenar_modelo(data, test_perc, randomstate, modelo_entrenar)
            model_data = convert_model_to_bytes(model)
            st.session_state.model_data = model_data
            st.divider()
            st.markdown("## Descarga tu modelo Entrenado")

        if 'model_data' in st.session_state:
            model_data = st.session_state.model_data
            if st.download_button("Descargar modelo PKL", model_data, file_name="modelo_entrenado.pkl", mime="application/octet-stream"):
                st.success("Modelo Guardado Correctamente")

def entrenar_modelo(data, test_perc, randomstate, modelo):
    x = data.drop("Abandono", axis=1)
    y = data["Abandono"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_perc/100, random_state=randomstate)
    
    model = modelo
    model.fit(x_train, y_train)
    
    y_pred_test = model.predict(x_test)
    y_pred_train = model.predict(x_train)
    
    col_metrica1, col_metrica2 = st.columns(2)
    with col_metrica1:
        st.metric("Precisión del Modelo (Test)", "{0:0.2f}".format(accuracy_score(y_test, y_pred_test)))
    with col_metrica2:
        st.metric("Precisión del Modelo (Train)", "{0:0.2f}".format(accuracy_score(y_train, y_pred_train)))
    st.divider()
    
    # Matriz de confusión

    col_fig1, col_fig2 = st.columns(2)
    with col_fig1:
        cm = confusion_matrix(y_test, y_pred_test)
        cm_matriz = pd.DataFrame(data=cm, columns=['Actual Positivo:1', 'Actual Negativo:0'],
                                 index=['Prediccion Positiva:1', 'Prediccion Negativa:0'])

        fig = ff.create_annotated_heatmap(z=cm_matriz.values, x=list(cm_matriz.columns),
                                          y=list(cm_matriz.index),
                                          colorscale='YlOrBr', showscale=True, reversescale=True)

        fig.update_layout(title='Matriz de Confusión', width=500, height=500)
        st.plotly_chart(fig)

    # Curva ROC AUC
    with col_fig2:
        y_pred1 = model.predict_proba(x_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred1, pos_label=True)
        roc_auc = roc_auc_score(y_test, y_pred1)
        
        trace0 = go.Scatter(x=fpr, y=tpr, mode='lines', name='Curva ROC (AUC = %0.2f)' % roc_auc)
        trace1 = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Clasificador Aleatorio', line={'dash': 'dash'})
        layout = go.Layout(title='Curva ROC', xaxis={'title': 'Tasa de Falsos Positivos'}, yaxis={'title': 'Tasa de Verdaderos Positivos'}, showlegend=True)
        fig = go.Figure(data=[trace0, trace1], layout=layout)
        fig.update_layout(width=500, height=500)

        st.plotly_chart(fig)

    return model


entrenamiento()