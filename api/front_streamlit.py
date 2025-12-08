import streamlit as st
import funtion as ft
import requests
from PIL import Image
import pandas as pd

# Título en la página
st.title("Frontend simple conectado a Flask")

menu = st.sidebar.selectbox("PÁGINAS", 
                            ("🏠 HOME", 
                             "🎯 PREDECIR", 
                             "🗄️ BASE DE DATOS", 
                             "🆔 PREDICCION POR ID"))

if menu == "🏠 HOME":
    mensaje = requests.get("http://127.0.0.1:5001/")
    st.subheader(mensaje.json())

elif menu == "🎯 PREDECIR":

    # Lector de imágenes
    uploaded_file1 = st.file_uploader(
        label="",
        type=["jpg", "png", "jpeg"],
        key="1"
    )

    if uploaded_file1:
        img = Image.open(uploaded_file1)  # Leer imagen con PIL
        
        if st.button("Ver imagen cargada"):
            st.image(img, use_container_width=True)

        st.markdown("---")

    # -------------------------------
    # Botón para enviar los datos al backend Flask
    # -------------------------------
        if st.button("Predecir"):
            # Conversión de imagen a un JSON
            datos = ft.imagen_a_json(img)

            # Llamamos al endpoint /predict de Flask
            prediccion = requests.post(
                "http://127.0.0.1:5001/predict", 
                json=datos
            )
            st.session_state["prediccion"] = prediccion

            # Mostramos el resultado en pantalla
            #st.write("Código HTTP:", respuesta.status_code)
            #st.write("Respuesta cruda:", respuesta.text)
            st.write("Predicción del modelo:", prediccion.json())
            #st.write("Clase:", resultado)
            
        if st.button("Guardar en la base de datos"):
            prediccion = st.session_state["prediccion"]

            datos_guardados = prediccion.json()

            # Llamamos al endpoint /predict de Flask
            respuesta = requests.post(
                "http://127.0.0.1:5001/predict_save", 
                json=datos_guardados
            )

            # Mostramos el resultado en pantalla
            #st.write("Código HTTP:", respuesta.status_code)
            #st.write("Respuesta cruda:", respuesta.text)
            st.write("Se ha guardado correctamente:", respuesta.json())
            #st.write("Clase:", resultado)

elif menu == "🗄️ BASE DE DATOS":
    #st.title
    if st.button("Mostrar base de datos"):
        tabla = requests.get("http://127.0.0.1:5001/show_data_base")
        st.write("Historial de predicciones:")
        df = pd.DataFrame(tabla.json())
        
        max = len(df)
        st.session_state["max"] = max
        
        st.dataframe(df[["id", "prediccion", "probabilidad", "date"]], use_container_width=True)

elif menu == "🆔 PREDICCION POR ID":
    st.subheader("Buscar prediccion por ID")
    tabla = requests.get("http://127.0.0.1:5001/show_data_base")
    df = pd.DataFrame(tabla.json())    
    max = len(df)

    id_buscar = st.number_input(
    "Ingrese el ID de la predicción:", 
    min_value=1, 
    max_value=max,
    step=1,
    )
    
    if (id_buscar<=max):
        if st.button("Buscar Prediccion"):
            respuesta = requests.get(f"http://127.0.0.1:5001/prediccion/{id_buscar}")

            data = respuesta.json()

            #st.write("Codigo HTTP", data.status_code)

            df = pd.DataFrame([{
                "id": data["id"],
                "prediccion": data["prediccion"],   # lo renombras aquí
                "probabilidad": data["probabilidad"],
                "date": data["date"]
            }])

            st.dataframe(df[["id", "prediccion", "probabilidad", "date"]], use_container_width=True)
                

#Primero ejecuta Flask:
#python app.py 
#Luego ejecuta Streamlit:
#streamlit run front_streamlit.py
#Streamlit enviará datos a Flask, Flask hará la predicción y Streamlit mostrará el resultado.