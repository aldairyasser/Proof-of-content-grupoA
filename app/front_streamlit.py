import streamlit as st
import funtion as ft

menu = st.sidebar.selectbox("PÁGINAS", 
                            ("🏠 HOME", 
                             "🎯 PREDECIR", 
                             "🗄️ BASE DE DATOS", 
                             "🆔 REGISTRO POR ID",
                             "🗑️ BORRAR PREDICCION POR ID",
                             "🌐 REGISTRO POR ID (QUERY)",
                             "🔥 PROBABILIDAD DE INCENDIO"))

if menu == "🏠 HOME":
    ft.home()

elif menu == "🎯 PREDECIR":
    ft.predecir()

elif menu == "🗄️ BASE DE DATOS":
    ft.mostrar_bd()

elif menu == "🆔 REGISTRO POR ID":
    ft.mostrar_bd_id()
    
elif menu == "🗑️ BORRAR PREDICCION POR ID":
    ft.borrar_prediccion_id()

elif menu == "🌐 REGISTRO POR ID (QUERY)":
    ft.registro_por_query()

elif menu == "🔥 PROBABILIDAD DE INCENDIO":
    ft.riesgo_incendio()


#Primero ejecuta Flask:
#python app.py 

#Luego ejecuta Streamlit:
#streamlit run front_streamlit.py
#Streamlit enviará datos a Flask, Flask hará la predicción y Streamlit mostrará el resultado.