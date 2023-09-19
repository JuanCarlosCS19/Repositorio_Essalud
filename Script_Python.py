import pandas as pd
import numpy as np
import streamlit as st
import pivottablejs as pt
st.set_page_config(page_title="Analisis Efectividad Essalud", page_icon=":bar_chart:", layout="wide")


# Supongamos que tienes un DataFrame llamado df que contiene tus datos
# Si aún no tienes un DataFrame, puedes cargar tus datos desde un archivo CSV o Excel.
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTnluyDGAkS8o-IezNn9dAEK9KKJa8ZkdbsLM6ijhyhlnm6-b5FEiXdfVPMsEL1qg/pub?gid=2015743116&single=true&output=csv")

# Elimina todas las columnas que contienen "CIM" en su nombre
df_cant = df.copy()
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
# df_vertical.to_clipboard()
tabla_dinamica = pd.pivot_table(df_vertical,
                                 values='Fecha de muestra',  # Puedes seleccionar cualquier columna numérica
                                 index=['Origen','Microorganismo', 'Interpretacion_Futuro', 'Medicamento_Antibiotico'],
                                 aggfunc='count')

# Resetear el índice para que los índices se conviertan en columnas
tabla_dinamica = tabla_dinamica.reset_index()
tabla_dinamica = tabla_dinamica.rename(columns={'Fecha de muestra': 'Recuento'})
tabla_dinamica = tabla_dinamica[tabla_dinamica["Interpretacion_Futuro"]!="-"]
df_filtered_v = tabla_dinamica
# df_filtered_v.to_clipboard()
# st.sidebar.header("Aplique los filtros aqui:")
# origen = st.sidebar.multiselect(
#         "Seleccione el origen:",
#         options=df_filtered_v["Origen"].unique()
#     )
# medicamento = st.sidebar.multiselect(
#         "Seleccione el medicamento:",
#         options=df_filtered_v["Medicamento_Antibiotico"].unique()
#     )
# microorganismo = st.sidebar.multiselect(
#         "Seleccione el microorganismo:",
#         options=df_filtered_v["Microorganismo"].unique()
#     )
# interpretacion = st.sidebar.multiselect(
#         "Seleccione la interpretacion:",
#         options=df_filtered_v["Interpretacion_Futuro"].unique()
#     )

# if origen:
#         df = df[df["Origen"].isin(origen)]


with st.container():
    st.title("ESSALUD - MICROBIOLOGIA")
    

    # Crear un contenedor con dos columnas
        
    st.header("", divider="grey")
    st.title("Analisis por Tipo Origen - Bacterias mas Frecuentes")
    st.write("Clasificacion R: RESISTENTE - S: SENSIBLE")
    top3_activate = st.checkbox("¿Desea activar el TOP3 Bacterias mas frecuentes?")
    origen_fil = st.multiselect(
        "Seleccione el ORIGEN:",
        options=df_filtered_v["Origen"].unique(),key="Origen_Frecuente"
    )
    df_selection_fil = df_cant
    if origen_fil:
        df_selection_fil = df_selection_fil[df_selection_fil["Origen"].isin(origen_fil)]
        df_cant = df_cant[df_cant["Origen"].isin(origen_fil)]

    
    st.write(f"Cantidad de registros para el ORIGEN :                   **{df_cant.shape[0]}** muestras", unsafe_allow_html=True)
    microorganismo_fil = st.multiselect(
        "Seleccione el MICROORGANISMO:",
        options=df_filtered_v["Microorganismo"].unique(),key="Microorganismo_Frecuente"
    )
    if microorganismo_fil:
        df_selection_fil = df_selection_fil[df_selection_fil["Microorganismo"].isin(microorganismo_fil)]
   

#     # Checkbox para mostrar/ocultar el DataFrame general
#     # mostrar_dataframe = st.checkbox("Mostrar Tabla General de Datos", value=False)

#     # if mostrar_dataframe:
        

#     #     ordenar_por = st.selectbox("Ordenar por:", df_vertical.columns)
#     #     df_sorted = df_vertical.sort_values(by=[ordenar_por])

#     #     # Mostrar la tabla en Streamlit
#     #     st.dataframe(df_sorted)
#     # Si el checkbox está seleccionado, muestra el DataFrame
#     # filtro = st.text_input("Filtrar por Medicamento Antibiótico:", "")
#     # filtro_microorganismo = st.text_input("Filtrar por Microorganismo", "")
#     # filtro_interpretacion = st.text_input("Filtrar por Interpretacion", "")


#     # Aplicar filtros secuencialmente a la tabla dinámica
    

#     # if filtro:
#     #     df_filtered_v = df_filtered_v[df_filtered_v['Medicamento_Antibiotico'].str.contains(filtro, case=False)]

#     # if filtro_microorganismo:
#     #     df_filtered_v = df_filtered_v[df_filtered_v['Microorganismo'].str.contains(filtro_microorganismo, case=False)]

#     # if filtro_interpretacion:
#     #     df_filtered_v = df_filtered_v[df_filtered_v['Interpretacion_Futuro'].str.contains(filtro_interpretacion, case=False)]

#     # # Ordenar la tabla dinámica por el recuento en orden descendente
#     # df_filtered_v = df_filtered_v.sort_values(by=['Recuento'], ascending=False)

#     # # Mostrar la tabla dinámica filtrada y ordenada
#     # st.write("Tabla Dinámica de Recuento (Ordenada por Recuento Descendente)")
#     # st.dataframe(df_filtered_v)

    
    

#     df_selection = df_filtered_v
#     if origen:
#         df_selection = df_selection[df_selection["Origen"].isin(origen)]
#     if medicamento:
#         df_selection = df_selection[df_selection["Medicamento_Antibiotico"].isin(medicamento)]
#     if microorganismo:
#         df_selection = df_selection[df_selection["Microorganismo"].isin(microorganismo)]
#     if interpretacion:
#         df_selection = df_selection[df_selection["Interpretacion_Futuro"].isin(interpretacion)]

#     df_selection = df_selection.sort_values(by=['Recuento','Interpretacion_Futuro'], ascending=[False, False])
#     total_recuento = df_selection["Recuento"].sum()

# # Calcular el porcentaje y agregarlo como una nueva columna
#     df_selection["Porcentaje"] = ((df_selection["Recuento"] / total_recuento) * 100).apply(lambda x: f"{x:.2f}%")
    
#     st.dataframe(df_selection)
#     df_sens_resis = df_selection.copy()
#     df_sens_resis = df_sens_resis[(df_sens_resis["Interpretacion_Futuro"] == "R") | (df_sens_resis["Interpretacion_Futuro"] == "S")]
#     df_sensible = df_sens_resis[df_sens_resis["Interpretacion_Futuro"]=="S"]
#     df_resistente = df_sens_resis[df_sens_resis["Interpretacion_Futuro"]=="R"]
#     col1, col2 = st.columns(2)
#     try:
#         valor_mas_sensible=df_sensible.iloc[0,3]
#     except:
#         valor_mas_sensible = "No se tienen datos para medicamentos sensibles"

#     try:
#         valor_mas_resistente=df_resistente.iloc[0,3]
#     except:
#         valor_mas_resistente = "No se tienen datos para medicamentos resistentes"
#     # Columna 1
#     with col1:
#         st.header("MEDICAMENTO MAS SENSIBLE")
#         st.write(f"EL MEDICAMENTO MAS SENSIBLE ES: {valor_mas_sensible}")

#     # Columna 2
#     with col2:
#         st.header("MEDICAMENTO MAS RESISTENTE")
#         st.write(f"EL MEDICAMENTO MAS RESISTENTE ES: {valor_mas_resistente}")


    st.title("")
    
    

    tabla_conteo = df_cant.groupby(["Origen", "Microorganismo"]).size().reset_index(name="Conteo")
    tabla_conteo = tabla_conteo.sort_values(by="Conteo", ascending=False)
    total_filas = tabla_conteo["Conteo"].sum()
    tabla_conteo["Porcentaje"] = (tabla_conteo["Conteo"] / total_filas * 100).apply(lambda x: f'{x:.2f}%')
    top3 = tabla_conteo.nlargest(3, 'Conteo')
    if top3_activate:
        tabla_conteo = tabla_conteo[tabla_conteo['Conteo'].isin(top3['Conteo'])]
        lista_top3 = top3.values.tolist()
        total_filas = tabla_conteo["Conteo"].sum()
        tabla_conteo["Porcentaje"] = (tabla_conteo["Conteo"] / total_filas * 100).apply(lambda x: f'{x:.2f}%')
        top3 = tabla_conteo.nlargest(3, 'Conteo')
        total_conteo = tabla_conteo["Conteo"].sum()
        total_porcentaje = tabla_conteo["Porcentaje"].str.rstrip('%').astype(float).sum()
    
    # Crear un DataFrame para los totales
        totales = pd.DataFrame({'Conteo': [total_conteo], 'Porcentaje': [f'{total_porcentaje:.2f}%']})
    
    # Concatenar el DataFrame de totales al DataFrame original
        tabla_conteo = pd.concat([tabla_conteo, totales], ignore_index=True)
        
        st.dataframe(tabla_conteo) #modificar tabla 

        





    else:
        total_filas = tabla_conteo["Conteo"].sum()
        tabla_conteo["Porcentaje"] = (tabla_conteo["Conteo"] / total_filas * 100).apply(lambda x: f'{x:.2f}%')
        top3 = tabla_conteo.nlargest(3, 'Conteo')
        total_conteo = tabla_conteo["Conteo"].sum()
        total_porcentaje = tabla_conteo["Porcentaje"].str.rstrip('%').astype(float).sum()
    
    # Crear un DataFrame para los totales
        totales = pd.DataFrame({'Conteo': [total_conteo], 'Porcentaje': [f'{total_porcentaje:.2f}%']})
    
    # Concatenar el DataFrame de totales al DataFrame original
        tabla_conteo = pd.concat([tabla_conteo, totales], ignore_index=True)
    
        st.dataframe(tabla_conteo)
    df_selection_fil = df_vertical
    if top3_activate:
        df_selection_fil = df_selection_fil[df_selection_fil["Microorganismo"].isin(tabla_conteo["Microorganismo"].to_list())]
    else:
        df_selection_fil = df_selection_fil

    # df_selection_fil.to_clipboard()

    filas = st.multiselect("Selecciona las filas:", ["Medicamento_Antibiotico","Fecha de muestra","Area","Muestra","Sexo"])
    df_selection_fil = df_selection_fil[df_selection_fil["Interpretacion_Futuro"].isin(["R","S"])]
    df_selection_fil["Recuento"] = 1
    if origen_fil:
        df_selection_fil = df_selection_fil[df_selection_fil["Origen"].isin(origen_fil)]
    if microorganismo_fil:
        df_selection_fil = df_selection_fil[df_selection_fil["Microorganismo"].isin(microorganismo_fil)]
    # columnas = st.multiselect("Selecciona las columnas:", df_selection_fil.columns)
    # valor = st.selectbox("Selecciona un valor:", df_selection_fil.columns)
    
    if 1:
                tabla_dinamica = pd.pivot_table(df_selection_fil, values="Recuento", index= filas, columns="Interpretacion_Futuro", aggfunc='count',fill_value=0)
                total_general = tabla_dinamica.sum().sum()

    # Calcular los porcentajes y agregarlos a la tabla dinámica
                tabla_porcentajes = tabla_dinamica.applymap(lambda x: f'{(x / total_general * 100):.2f}%' if x != 0 else '')
                nuevos_nombres_columnas = {
        'R': '% Resistente',
        'S': '% Sensible'
    }
                
                tabla_porcentajes = tabla_porcentajes.rename(columns=nuevos_nombres_columnas)

    # Concatenar la tabla de porcentajes a la tabla dinámica original
                tabla_dinamica = pd.concat([tabla_dinamica, tabla_porcentajes], axis=1)

                try:
                    tabla_dinamica = tabla_dinamica.sort_values(by='S', ascending=False)
                except:
                     pass
                def highlight_max(s):
                    is_max = s == s.max()
                    background_color = 'background-color: darkred'
                    text_color = 'color: white'
                    styles = [background_color if v else '' for v in is_max]
                    styles[0] += f'; {text_color}'  # Aplicar estilo de texto blanco al primer valor
                    return styles

# Aplicar el estilo condicional a las columnas donde deseas resaltar los valores más altos
                columnas_resaltar = ['% Resistente', '% Sensible']  # Aquí puedes especificar las columnas que deseas resaltar
                if ('% Resistente' in (tabla_dinamica.columns.tolist())) and ('% Sensible' in (tabla_dinamica.columns.tolist())):
                    st.write(tabla_dinamica.style.apply(highlight_max, subset=columnas_resaltar))
                elif "% Resistente" in (tabla_dinamica.columns.tolist()):
                    st.write(tabla_dinamica.style.apply(highlight_max, subset=["% Resistente"]))
                elif "% Sensible" in (tabla_dinamica.columns.tolist()):
                    st.write(tabla_dinamica.style.apply(highlight_max, subset=["% Sensible"]))

                     
              
    # st.write("La tabla dinámica solicitada no funciono")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
