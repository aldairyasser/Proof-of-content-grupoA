import streamlit as st
import funtion as ft
import requests
from PIL import Image

# Título en la página
st.title("Frontend simple conectado a Flask")

# Entradas numéricas para que el usuario escriba los valores

'''
Streamlit
    - Lee la imagen ✅
    - Mostrar imagen ✅
    - La convierte a base64
    - La envía a Flask

Flask
    - Decodifica base64 --> bytes
    - Convierte bytes --> imagen
    - Preprocesa igual que en entrenamiento (resize, /255)
    - Llama al modelo
    - Devuelve resultado
'''

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
        respuesta = requests.post(
            "http://127.0.0.1:5000/predict", 
            json=datos
        )

        # Mostramos el resultado en pantalla
        st.write("Código HTTP:", respuesta.status_code)
        st.write("Respuesta cruda:", respuesta.text)
        st.write("Predicción del modelo:", respuesta.json())
        #st.write("Clase:", resultado)

    # ANALIZAR RIESGO DE INCENDIO
    if st.button("Analizar riesgo de incendio"):
        datos = ft.imagen_a_json(img)
        respuesta = requests.post(
            "http://127.0.0.1:5000/fire_probability",
            json=datos
        )

        st.write("Código HTTP:", respuesta.status_code)
        st.write("Respuesta cruda:", respuesta.text)

        try:
            st.write("Resultado riesgo:", respuesta.json())
        except:
            st.error("El servidor no devolvió JSON válido.")

    # ESTADO DEL SERVIDOR
    if st.button("Estado del servidor"):
        respuesta = requests.get("http://127.0.0.1:5000/health")

        st.write("Código HTTP:", respuesta.status_code)
        st.write("Respuesta cruda:", respuesta.text)

        try:
            st.write("Estado:", respuesta.json())
        except:
            st.error("El servidor no devolvió JSON válido.")

    # INFORMACIÓN COMPLETA DEL SERVICIO
    if st.button("Información del sistema"):
        respuesta = requests.get("http://127.0.0.1:5000/info")

        st.write("Código HTTP:", respuesta.status_code)
        st.write("Respuesta cruda:", respuesta.text)

        try:
            st.write("Información:", respuesta.json())
        except:
            st.error("El servidor no devolvió JSON válido.")


#Primero ejecuta Flask:
#python app.py 
#Luego ejecuta Streamlit:
#streamlit run front_streamlit.py
#Streamlit enviará datos a Flask, Flask hará la predicción y Streamlit mostrará el resultado.