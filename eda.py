import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
import seaborn as sns
from io import StringIO

def eda():

    st.markdown("# :bar_chart: Análisis Explotario de Datos")
    st.write("""
            En este análisis exploratorio de datos, nos enfocaremos en 
            comprender las variables y patrones subyacentes que 
            afectan el abandono de los clientes. 
        """)
    
    st.divider()

    if "df" not in st.session_state:
        st.image("images/upload-cloud-data.png", width=300)
        st.write("Debe Ingresar el dataset primero, Dirijase a la pagina principal.")
        st.divider()

    else:
        #data = pd.read_csv(r"datasets/dataset_abandono.csv")
        data = st.session_state.df

        seleccion_grafica_cate = st.sidebar.selectbox('Selecciona una Variable Categórica', list(data.select_dtypes(include='object').columns))
        seleccion_grafica_nume = st.sidebar.selectbox('Selecciona una Variable Numérica', list(data.select_dtypes(exclude='object').columns),index=2)

        st.markdown("## Metricas de los datos")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Número de Filas", data.shape[0])
        col2.metric("Número de Columnas", data.shape[1])
        col3.metric("Datos Duplicados", data.duplicated().sum())
        col4.metric("Variables Categóricas",data.select_dtypes(include='object').shape[1])
        col5.metric("Variables Numéricas",data.select_dtypes(exclude='object').shape[1])

        st.divider()

        st.markdown('## Gráficos de los Datos')

        c1, c2 = st.columns((5,5))
        valores_categoricas = data[seleccion_grafica_cate].value_counts()
        valores_numericas = data[seleccion_grafica_nume]
        colorscale = px.colors.sequential.YlOrBr
        num_categorias = len(valores_categoricas.index)
        step_size = int(len(colorscale) / num_categorias)
        colores = list(colorscale[::step_size])

        with c1:
            st.bar_chart(data=valores_categoricas, x=None, y='count', color=None)

        with c2:
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')

            wedges, texts, autotexts = ax.pie(
                valores_categoricas.values,
                labels=valores_categoricas.index,
                autopct='%1.1f%%',
                startangle=140
            )

            ax.set_title(f'Gráfico Circular - {seleccion_grafica_cate}', fontsize=15, color='white')
            plt.tight_layout()
            ax.patch.set_alpha(0.0)
            fig.patch.set_alpha(0.0)
            st.pyplot(fig)


        st.divider()


        gra1,gra2 = st.columns((5,5))

        with gra1:
            fig_box = go.Figure()

            for variable, color in zip(data[seleccion_grafica_cate].unique(), colores):
                fig_box.add_trace(go.Box(
                    x=data[seleccion_grafica_cate][data[seleccion_grafica_cate] == variable],
                    y=data[seleccion_grafica_nume][data[seleccion_grafica_cate] == variable],
                    name=variable,
                    marker=dict(color=color),
                    hovertemplate='%{x}: %{y}'
                ))

            fig_box.update_layout(
                title=f"Gráfico Boxplot - {seleccion_grafica_cate}",
                xaxis_title=seleccion_grafica_cate,
                yaxis_title=seleccion_grafica_nume,
                font=dict(size=12),
                width=500,
                height=500
            )

            st.plotly_chart(fig_box)


        def sturges_rule(data):
            n = len(data)
            k = 1 + math.log2(n)
            return int(k)


        with gra2:
            fig_hist = go.Figure()
            k = sturges_rule(valores_numericas)
            fig_hist.add_trace(go.Histogram(
                x=valores_numericas,
                nbinsx=k,
                marker=dict(color=colores[0]),
                hovertemplate='Edad: %{x}<br>valores_categoricas: %{y}'
            ))

            fig_hist.update_layout(
                title=f"Histograma - {seleccion_grafica_nume}",
                xaxis_title=seleccion_grafica_nume,
                yaxis_title="Frecuencia",
                font=dict(size=12),
                width=500,
                height=500
            )

            st.plotly_chart(fig_hist)

        st.divider()

        data_corr = data.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(7, 6), facecolor='none') 
        heatmap = sns.heatmap(data_corr, annot=True, cmap='YlOrBr', fmt='.2f', ax=ax, cbar=False) 

        ax.set_title('Mapa de Calor - Matriz de correlación', fontsize=15, color='white',fontfamily='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=10, color='white')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10, color='white')

        plt.tight_layout()

        ax.patch.set_alpha(0.0)
        fig.patch.set_alpha(0.0)
        ax.spines[:].set_color('white')
        ax.tick_params(colors='white')

        st.pyplot(fig)


        st.divider()


        binary_df = data.isnull().astype(int)

        fig = go.Figure()

        fig.add_trace(go.Heatmap(z=binary_df.values,
                                x=binary_df.columns,
                                y=binary_df.index,
                                colorscale='YlOrBr',
                                showscale=False))

        fig.update_layout(
            title="Datos nulos en los Datos",
            xaxis_title="Columnas",
            yaxis_title="Índice",
            font=dict(size=12),
            width=1100,
            height=600
        )

        st.plotly_chart(fig)


        st.divider()


        st.markdown('## Información sobre los Datos')
        col_resu1, col_resu2 = st.columns(2)
        with col_resu1:
            st.markdown("### Resumen Conciso de los Datos")
            if st.checkbox("Mostrar Resumen"):
                info = StringIO()
                data.info(buf=info)
                st.text(str(info.getvalue()))
            
        with col_resu2:
            st.markdown("### Datos Nulos por Columnas")
            if st.checkbox("Mostrar Datos Nulos"):
                st.write(data.isnull().sum().sort_values(ascending=False))


        st.divider()    


        col_resu3, col_resu4 = st.columns((2))
        with col_resu3:
            st.markdown("### Correlación Entre Variables Numéricas")
            if st.checkbox("Mostrar Correlación"):  
                st.write(data.corr(numeric_only=True))
        with col_resu4:
            st.markdown("### Estadística Descriptiva de los Datos")
            if st.checkbox("Mostrar Estadística"):
                st.write(data.describe().round(2))


eda()