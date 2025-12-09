import base64
import streamlit as st
import mimetypes
from io import BytesIO
from PIL import Image
import requests
from PIL import Image
import pandas as pd
import os

st.set_page_config(
    page_title="Clasificador Geoespacial",
    page_icon="🛰️",
    layout="centered"
)

# Función de la pantalla home 
def home():
    if requests.get("http://127.0.0.1:5001/"):

        # ---- Hero Section ----
        st.markdown("""
            <div style='text-align:center;'>
                <h1 style='font-size:48px; margin-bottom:10px;'>FireVision AI</h1>
                <h3 style='margin-top:-10px; color:#FF4B4B;'>Detección Temprana de Riesgo de Incendio</h3>
                <p style='font-size:20px; opacity:0.85;'>
                    Un sistema inteligente para anticipar incendios antes de que ocurran.
                </p>
            </div>
        """, unsafe_allow_html=True)

        base_path = os.path.dirname(os.path.realpath(__file__))

        # Construir la ruta al modelo dentro de la carpeta "modelos"
        model_path = os.path.join(base_path, 'img', 'portada.jpeg')
        st.image(model_path, use_container_width="auto")

        st.markdown("---")

        # ---- CONTEXTO ----
        st.markdown("""
            <h2>🌍 Contexto</h2>
            <div class="tarjeta">
                <p style="font-size:17px;">
                    Los incendios forestales están aumentando en frecuencia, escala e intensidad.
                    Instituciones públicas y privadas — aseguradoras eléctricas, parques naturales,
                    gobiernos — necesitan anticiparse, no reaccionar cuando ya es tarde.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ---- EL PROBLEMA ----
        st.markdown("""
            <h2> - El Problema</h2>
            <div class="tarjeta">
                <ul style="font-size:17px;">
                    <li>No saben qué áreas están más secas o degradadas.</li>
                    <li>No cuentan con un mapa dinámico del estado real del terreno.</li>
                    <li>No pueden priorizar brigadas, mantenimiento o inspecciones.</li>
                </ul>
                <p style="font-size:17px;">
                    🔻 Esto provoca sobrecostes, incendios millonarios, multas ambientales
                    y riesgos para vidas humanas.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ---- OPORTUNIDAD ----
        st.markdown("""
            <h2> - La Oportunidad</h2>
            <div class="tarjeta">
                <p style="font-size:17px;">
                    FireVision AI combina la clasificación automática del terreno con el análisis
                    visual de sequedad para crear un mapa real del riesgo de incendio.
                </p>
                <p style="font-size:17px;">
                    Esta tecnología permite <b>predecir zonas críticas</b> con antelación y tomar decisiones
                    preventivas de forma automatizada.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ---- LA SOLUCIÓN ----
        st.markdown("""
            <h2> - La Solución: <span style='color:#88e788;'>FireVision AI</span></h2>
            <div class="tarjeta">
                <ul style="font-size:17px;">
                    <li>📌 Clasificación automática del terreno.</li>
                    <li>🌡️ Detector visual de sequedad (índice de marrón).</li>
                    <li>📍 Geolocalización inteligente.</li>
                    <li>🔥 Cálculo de riesgo por píxel o por zona (0–100).</li>
                </ul>
                <h4> - ¿Cómo funciona?</h4>
                <ol style="font-size:17px;">
                    <li>Cargas una imagen satelital o aérea.</li>
                    <li>El sistema identifica el tipo de terreno.</li>
                    <li>Analiza la sequedad y la vegetación degradada.</li>
                    <li>Calcula un índice de probabilidad de incendio.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

        # ---- CASO REAL ----
        st.markdown("""
            <h2>🛰️ Caso Profesional — <b>SierraLuz</b> 🛰️</h2>
            <div class="tarjeta">
                <h4> - Problema</h4>
                <p style="font-size:17px;">
                    SierraLuz gestiona <b>2.800 km de líneas eléctricas</b> en zonas forestales.
                    En 2024 sufrió 3 incendios por vegetación seca, perdiendo más de <b>18 millones de euros</b>.
                </p>
                <h4> - Solución implementada</h4>
                <ul style="font-size:17px;">
                    <li>Clasificación automática del terreno.</li>
                    <li>Detección del nivel de sequedad visual.</li>
                    <li>Cálculo del índice de riesgo 0–100.</li>
                    <li>Alertas y reportes automáticos de zonas críticas.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # ---- VALOR EMPRESARIAL ----
        st.markdown("""
            <h2>💼 ¿Por qué las empresas pagan por esto?</h2>
            <div class="tarjeta">
                <ul style="font-size:17px;">
                    <li>Reduce riesgo legal y financiero.</li>
                    <li>Evita incendios millonarios.</li>
                    <li>Ofrece valor inmediato y continuo (modelo SaaS).</li>
                    <li>Es simple, visual y totalmente automatizado.</li>
                </ul>
                <p style="font-size:20px; text-align:center; margin-top:20px; color:#FF4B4B;">
                    “Es más barato pagar FireVision AI que pagar un incendio.”
                </p>
            </div>
        """, unsafe_allow_html=True)

# Función para convertir una imagena a json (se usa en la siguiente función)
def imagen_a_json(imagen):
    buffer = BytesIO()
    
    formato = imagen.format if imagen.format is not None else "JPEG"
    imagen.save(buffer, format=formato)

    imagen_bytes = buffer.getvalue()
    imagen_codificada = base64.b64encode(imagen_bytes).decode("utf-8")

    return {
        "imagen_base64": imagen_codificada
    }

# Función que predice una imagen pasado del front (PATH) (POST)
def predecir():
    st.subheader("🌄 Clasificador de biomas 🏞️")

    base_path = os.path.dirname(os.path.realpath(__file__))

    # Construir la ruta al modelo dentro de la carpeta "modelos"
    test_path = os.path.join(base_path, 'data', 'test.zip')
    with st.expander("Descargar imágenes de test", icon='📷'):
        with open(test_path, "rb") as f:
            st.download_button(
                label="Descargar ZIP con imágenes de test",
                data=f,
                file_name="test_images.zip",
                mime="application/zip",
                icon='📥'
            )
    # Lector de imágenes
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    uploaded_file1 = st.file_uploader(
        label="Selecione una imagen:",
        type=["jpg", "png", "jpeg"],
        key="1"
    )

    img = None

    if uploaded_file1:
        img = Image.open(uploaded_file1)
        
        if st.button("Ver imagen cargada", icon='🖼️'):
            st.image(img, width="stretch")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            predecir_btn = st.button("Predecir", width="stretch", icon='🪄')

        with col2:
            guardar_btn = st.button("Guardar predicción", width="stretch", icon='💾')

    # --------------------------------------------
    # Botón para enviar los datos al backend Flask
    # --------------------------------------------
        if predecir_btn:
            # Llamaos a la funcion de conversión de imagen a un JSON
            datos = imagen_a_json(img)

            # Consumimos al endpoint /predict de Flask
            prediccion = requests.post(
                "http://127.0.0.1:5001/predict", 
                json=datos
            )

            st.session_state["prediccion"] = prediccion

            resultado = prediccion.json()
            clase = resultado["clase_nombre"]
            probs = resultado["probabilidades"]

            st.success(f"🎯 **Clase predicha:** {clase}")
            st.success(f"％ **Probabilidad:** {probs:.2f}") # Futura a mejora if <50% que rojo (st.error) y amarillo (st.warning)

            # Mostramos el resultado en front la predicción
            #st.write("Predicción del modelo:", prediccion.json())
            #st.write("Código HTTP:", respuesta.status_code)
            #st.write("Respuesta cruda:", respuesta.text)
            #st.write("Clase:", resultado)
        
        # Boton para guardar la predicción en base de datos
        if guardar_btn:
            prediccion = st.session_state["prediccion"]

            if "prediccion" not in st.session_state:
                st.error("Primero debes predecir la imagen.")
            else:
                pred = st.session_state["prediccion"].json()
                respuesta = requests.post(
                    "http://127.0.0.1:5001/predict_save", 
                    json=pred
                )
                st.success("Guardado correctamente con:")
                st.write(respuesta.json())

            # Mostramos el resultado en pantalla
            #st.write("Código HTTP:", respuesta.status_code)
            #st.write("Respuesta cruda:", respuesta.text)
            #st.write("Se ha guardado correctamente:", respuesta.json())
            #st.write("Clase:", resultado)

# Función que muestra toda la base de datos (Conección por query / GET)
def mostrar_bd():
    st.subheader("📂 Historial de predicciones 🗂️")

    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)

    tabla = requests.get("http://127.0.0.1:5001/show_data_base")
    df = pd.DataFrame(tabla.json())

    st.dataframe(df[["id", "prediccion", "probabilidad", "fecha"]], width="stretch")

# Función que devuelve la BD por id (Conección por argumento) / Query
def mostrar_bd_id():
    st.subheader("🔎 Buscar predicción por ID 🔍")
    
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    tabla = requests.get("http://127.0.0.1:5001/show_data_base")
    df = pd.DataFrame(tabla.json())    
    max_id = df["id"].max()

    id_buscar = st.number_input(
        "Ingrese el ID :", 
        min_value=1, 
        max_value=max_id,
        step=1,
    )
    st.caption("⚠️ Nota: Los IDs pueden no ser consecutivos si ya se han eliminado registros.")

    if st.button("Buscar Predicción", icon='🔎'):
        respuesta = requests.get(f"http://127.0.0.1:5001/predict/{id_buscar}")
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            df_result = pd.DataFrame([{
                "id": data["id"],
                "prediccion": data["prediccion"],
                "probabilidad": data["probabilidad"],
                "fecha": data["fecha"]
            }])
            st.dataframe(df_result, width="stretch")
        else:
            st.error("‼️ Registro no encontrado, pruebe con otro ‼️")

# Borrar predicción por id (Conección por argumento)
def borrar_prediccion_id():
    st.subheader("🗑️ Borrar predicción por ID")
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)

    # Función auxiliar
    def cargar_bd():
        tabla = requests.get("http://127.0.0.1:5001/show_data_base")
        return pd.DataFrame(tabla.json())

    # Guardar BD en session_state para actualizar automaticamente
    if "df_bd" not in st.session_state:
        st.session_state["df_bd"] = cargar_bd()

    df = st.session_state["df_bd"]

    st.markdown("### 📂 Base de datos actual")
    st.dataframe(df[["id", "prediccion", "probabilidad", "fecha"]], width='stretch')
    
    if df.empty:
        st.warning("⚠️ La base de datos está vacía.")
    
    st.markdown("---")

    max_id = df["id"].max()

    id_borrar = st.number_input("ID a eliminar:", min_value=1, max_value=max_id, step=1)
    st.caption("⚠️ Nota: Los IDs pueden no ser consecutivos si ya se han eliminado registros.")


    if st.button("Eliminar Predicción", type="primary", icon='🗑️'):
        respuesta = requests.delete(f"http://127.0.0.1:5001/delete_predict/{id_borrar}")

        if respuesta.status_code == 200:
            st.success("Predicción eliminada correctamente")
            st.session_state["df_bd"] = cargar_bd()  # recarga BD
            st.rerun()
        else:
            st.error("Error eliminando el registro")

# Función que devuelve el registro por id por query
def registro_por_query():
    st.subheader("🔎 Consultar predicción por URL (Query)")

    st.markdown("""
        <div class="tarjeta">
            <p style='font-size:16px;'>
                Introduce la URL del endpoint que deseas consultar.<br>
                Estructura:<br>
                <code>http://127.0.0.1:5001/prediccion_query?id=5</code>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Campo de entrada elegante
    url = st.text_input(
        "URL del endpoint:",
        value="",
        placeholder="Introduce aquí una URL válida",
        icon='📎'
    )

    st.markdown("---")

    # Botón centrado y más estético
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        ejecutar = st.button("Mostrar contenido", type="primary", icon='🔍')

    if ejecutar:
        try:
            respuesta = requests.get(url)

            st.markdown("### Respuesta del servidor")

            # Intentamos mostrar JSON
            try:
                st.json(respuesta.json())
            except:
                st.text(respuesta.text)

        except Exception as e:
            st.error(f"❌ Error de conexión: {str(e)}")

def riesgo_incendio():
    st.subheader("🔥 Detección de Riesgo de Incendio 🌲")

    base_path = os.path.dirname(os.path.realpath(__file__))

    # ZIP de imágenes de ejemplo (opcional)
    test_path = os.path.join(base_path, 'data', 'test_incendio.zip')

    with st.expander("Descargar imágenes de ejemplo", icon='📷'):
        with open(test_path, "rb") as f:
            st.download_button(
                label="Descargar imágenes de prueba",
                data=f,
                file_name="test_incendio.zip",
                mime="application/zip",
                icon='📥'
            )
    # --------------------------------------------
    # Cargar imagen
    # --------------------------------------------
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Sube una imagen de vegetación o paisaje:",
        type=["jpg", "jpeg", "png"],
        key="fire1"
    )

    img = None

    if uploaded_file:
        img = Image.open(uploaded_file)

        if st.button("Ver imagen cargada", icon='🖼️'):
            st.image(img, width="stretch")

        st.markdown("---")

        analizar_btn = st.button("Analizar riesgo", width="stretch", icon='🔥')

        # --------------------------------------------
        # PETICIÓN AL ENDPOINT fire_probability
        # --------------------------------------------
        if analizar_btn:

            # Convertimos imagen a base64
            datos = imagen_a_json(img)  # Si ya tienes esta función, úsala

            respuesta = requests.post(
                "http://127.0.0.1:5001/fire_probability",
                json=datos
            )

            result = respuesta.json()

            marron = result["porcentaje_marron"]
            verde = result["porcentaje_verde"]
            riesgo = result["nivel_riesgo_incendio"]

            # -----------------------------------
            # Estética del resultado
            # -----------------------------------
            st.markdown("### 🔍 Resultado del análisis")

            if riesgo == "Alto":
                st.error(f"🔥 **RIESGO ALTO DE INCENDIO**")
            elif riesgo == "Medio":
                st.warning(f"⚠️ **RIESGO MEDIO DE INCENDIO**")
            else:
                st.success(f"🌿 **RIESGO BAJO DE INCENDIO**")

            st.markdown(
                f"""
                <div style="padding:15px; border-radius:12px;">
                    <p><b>Porcentaje marrón:</b> {marron:.2%}</p>
                    <p><b>Porcentaje verde:</b> {verde:.2%}</p>
                </div>
                """,
                unsafe_allow_html=True
            )