import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(page_title="Analisis Efectividad Essalud", page_icon=":bar_chart:", layout="wide")


# Supongamos que tienes un DataFrame llamado df que contiene tus datos
# Si aún no tienes un DataFrame, puedes cargar tus datos desde un archivo CSV o Excel.
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTnluyDGAkS8o-IezNn9dAEK9KKJa8ZkdbsLM6ijhyhlnm6-b5FEiXdfVPMsEL1qg/pub?gid=1667552343&single=true&output=csv", sheet_name=0)

# Elimina todas las columnas que contienen "CIM" en su nombre
columnas_cim = [col for col in df.columns if "CIM" in col]
df = df.drop(columns=columnas_cim)

# Lista de las palabras clave que deseas buscar en los nombres de las columnas
palabras_clave = ["Interpretación"]

# Filtra las columnas que contienen las palabras clave
columnas_seleccionadas = [col for col in df.columns if any(palabra in col for palabra in palabras_clave)]

# Crea un nuevo DataFrame con todas las otras columnas y las seleccionadas en formato vertical
df_vertical = pd.melt(df, id_vars=[col for col in df.columns if col not in columnas_seleccionadas],
                      value_vars=columnas_seleccionadas, var_name="Nombre de la Columna", value_name="Valor")

# Cambiar el tipo de datos de la columna "Fecha de nacimiento" a datetime
df_vertical['Fecha de nacimiento'] = pd.to_datetime(df_vertical['Fecha de nacimiento'], errors='coerce')

# Renombrar las columnas
df_vertical = df_vertical.rename(columns={'Nombre de la Columna': 'Medicamento_Antibiotico', 'Valor': 'Interpretacion_Origen'})

df_vertical['Interpretacion_Futuro'] = df_vertical['Interpretacion_Origen']

# Realizar las transformaciones
df_vertical['Interpretacion_Futuro'].replace({'S*': 'S', 'R*': 'R', 'I': 'I', 'IB': 'I', np.nan: '-'}, inplace=True)
df_vertical['Medicamento_Antibiotico'] = df_vertical['Medicamento_Antibiotico'].str.replace(' Interpretación', '')
tabla_dinamica = pd.pivot_table(df_vertical,
                                 values='Fecha de muestra',  # Puedes seleccionar cualquier columna numérica
                                 index=['Microorganismo', 'Interpretacion_Futuro', 'Medicamento_Antibiotico'],
                                 aggfunc='count')

# Resetear el índice para que los índices se conviertan en columnas
tabla_dinamica = tabla_dinamica.reset_index()
tabla_dinamica = tabla_dinamica.rename(columns={'Fecha de muestra': 'Recuento'})
tabla_dinamica = tabla_dinamica[tabla_dinamica["Interpretacion_Futuro"]!="-"]

st.header("ESSALUD", divider="grey")
st.title("Analisis Medicamentos para Microorganismos")
st.write("Tabla General de Datos")

# Checkbox para mostrar/ocultar el DataFrame general
mostrar_dataframe = st.checkbox("Mostrar Tabla General de Datos", value=False)

if mostrar_dataframe:
    

    ordenar_por = st.selectbox("Ordenar por:", df_vertical.columns)
    df_sorted = df_vertical.sort_values(by=[ordenar_por])

    # Mostrar la tabla en Streamlit
    st.dataframe(df_sorted)
# Si el checkbox está seleccionado, muestra el DataFrame
# filtro = st.text_input("Filtrar por Medicamento Antibiótico:", "")
# filtro_microorganismo = st.text_input("Filtrar por Microorganismo", "")
# filtro_interpretacion = st.text_input("Filtrar por Interpretacion", "")


# Aplicar filtros secuencialmente a la tabla dinámica
df_filtered_v = tabla_dinamica

# if filtro:
#     df_filtered_v = df_filtered_v[df_filtered_v['Medicamento_Antibiotico'].str.contains(filtro, case=False)]

# if filtro_microorganismo:
#     df_filtered_v = df_filtered_v[df_filtered_v['Microorganismo'].str.contains(filtro_microorganismo, case=False)]

# if filtro_interpretacion:
#     df_filtered_v = df_filtered_v[df_filtered_v['Interpretacion_Futuro'].str.contains(filtro_interpretacion, case=False)]

# # Ordenar la tabla dinámica por el recuento en orden descendente
# df_filtered_v = df_filtered_v.sort_values(by=['Recuento'], ascending=False)

# # Mostrar la tabla dinámica filtrada y ordenada
# st.write("Tabla Dinámica de Recuento (Ordenada por Recuento Descendente)")
# st.dataframe(df_filtered_v)

st.sidebar.header("Aplique los filtros aqui:")
medicamento = st.sidebar.multiselect(
    "Seleccione el medicamento:",
    options=df_filtered_v["Medicamento_Antibiotico"].unique()
)
microorganismo = st.sidebar.multiselect(
    "Seleccione el microorganismo:",
    options=df_filtered_v["Microorganismo"].unique()
)
interpretacion = st.sidebar.multiselect(
    "Seleccione la interpretacion:",
    options=df_filtered_v["Interpretacion_Futuro"].unique()
)

df_selection = df_filtered_v.query(
    "Medicamento_Antibiotico == @medicamento | Microorganismo == @microorganismo | Interpretacion_Futuro == @interpretacion"
)
df_selection = df_selection.sort_values(by=['Recuento'], ascending=False)

st.dataframe(df_selection)

css = """
<style>
body {
    background-color: #FF0000; /* Cambia el código de color aquí */
}
</style>
"""

# Agregar el CSS personalizado
st.markdown(css, unsafe_allow_html=True)
