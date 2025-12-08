import streamlit as st
import funtion as ft

menu = st.sidebar.selectbox("PÁGINAS", 
                            ("🏠 HOME", 
                             "🎯 PREDECIR", 
                             "🗄️ BASE DE DATOS", 
                             "🆔 PREDICCION POR ID"))

if menu == "🏠 HOME":
    ft.home()

elif menu == "🎯 PREDECIR":
    ft.predecir()

elif menu == "🗄️ BASE DE DATOS":
    ft.mostrar_bd()

elif menu == "🆔 PREDICCION POR ID":
    ft.mostrar_bd_id()

#Primero ejecuta Flask:
#python app.py 

#Luego ejecuta Streamlit:
#streamlit run front_streamlit.py
#Streamlit enviará datos a Flask, Flask hará la predicción y Streamlit mostrará el resultado.