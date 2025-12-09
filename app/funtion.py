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

    st.title("Proof Of Content (PoC)")
    # Ruta absoluta del archivo actual
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Construir la ruta al modelo dentro de la carpeta "modelos"
    model_path = os.path.join(base_path, 'img', 'portada1.jpeg')
    st.image(model_path, use_container_width="auto")

    if requests.get("http://127.0.0.1:5000/"):
        st.markdown('''
## 🔥 FireVision AI — Detección Temprana de Riesgo de Incendio 🛰️

---

### 🌍 Contexto  
Los incendios forestales son cada vez más frecuentes e intensos. Gobiernos, aseguradoras, eléctricas y parques naturales requieren **pronosticar el riesgo**, no reaccionar demasiado tarde.  
Hoy dependen de mapas desactualizados, inspecciones manuales y reportes incompletos.  
No existe un sistema visual automatizado a escala real… hasta ahora.

---

## 🚨 El Problema
- No saben qué áreas están más secas o degradadas.  
- No cuentan con un mapa dinámico basado en el estado real del terreno.  
- No pueden priorizar brigadas, seguros o mantenimiento eléctrico.  

🔻 Esto genera sobrecostos, pérdidas millonarias, multas ambientales y riesgos para vidas y propiedades.

---

## 🌟 La Oportunidad  
Tu tecnología ya clasifica terrenos (bosque, prado, chaparral, montaña…).  
Al añadir un análisis automático de **marronización** (vegetación seca), puedes crear un mapa real de probabilidad de incendio basado en apariencia visual actual.

---

## 🚀 La Solución: **FireVision AI**  
Plataforma que combina:

- Clasificación automática del terreno.  
- Detector visual de sequedad (índice de marrón).  
- Geolocalización inteligente.  
- Cálculo de riesgo por píxel o por zona.

### **Cómo funciona**
1. Cargas una imagen satelital/aérea.  
2. Se clasifica el tipo de terreno.  
3. Se analiza la sequedad:  
   - porcentaje de marrón  
   - textura de vegetación seca  
   - combustible natural acumulado  
4. Se calcula un **índice de probabilidad de incendio (0–100)**.  

Ejemplos:  
- **Bosque + baja sequedad → Riesgo Bajo**  
- **Prado seco + alta marronización → Riesgo Alto**  
- **Chaparral + sequedad moderada → Riesgo Medio-Alto**

---

# 📊 Caso Profesional — Cliente: **Compañía Eléctrica SierraLuz**

### Problema
SierraLuz opera **2,800 km de líneas eléctricas** en zonas forestales.  
Tras 3 incendios en 2024 por vegetación seca, perdió **USD 18 millones**.  
Necesitaban identificar puntos críticos y priorizar mantenimiento.

### Solución aplicada con FireVision AI

**Paso 1 — Clasificación del terreno**  
bosque | chaparral | prado | desierto

**Paso 2 — Detección de sequedad visual**  
Análisis de marrón, textura y cambios mes a mes.

**Paso 3 — Cálculo de riesgo (0–100)**

**Paso 4 — Acciones automáticas**  
- Reporte semanal a equipos  
- Priorización de zonas rojas  
- Alertas de evolución del riesgo  

---

## 🎯 Resultados para SierraLuz

- 🔻 **61% menos incendios causados por vegetación seca**  
- 💰 **Ahorro anual: USD 7.4 millones**  
- 🚚 **Mantenimiento 50% más eficiente**  
- 🤝 Contrato renovado: **USD 450,000 / año**  

---

## 💼 ¿Por qué las empresas pagan por esto?

- Reduce riesgo legal y financiero.  
- Evita incendios millonarios.  
- Es simple, visual, automatizado y recurrente (SaaS).  

💬 *“Es más barato pagar FireVision AI que pagar un incendio.”*

''')
    else:
        st.subheader("Conectando...")


    '''Explicar storytelling y caso de uso'''

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

    with st.expander("📥 Descargar imágenes de test"):
        with open("./data/test.zip", "rb") as f:
            st.download_button(
                label="Descargar ZIP con imágenes de test",
                data=f,
                file_name="test_images.zip",
                mime="application/zip"
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
        img = Image.open(uploaded_file1)  # Leer imagen con PIL
        
        if st.button("Ver imagen cargada"):
            st.image(img, width="stretch")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            predecir_btn = st.button("🔍 Predecir", width="stretch")

        with col2:
            guardar_btn = st.button("💾 Guardar predicción", width="stretch")

    # --------------------------------------------
    # Botón para enviar los datos al backend Flask
    # --------------------------------------------
        if predecir_btn:
            # Llamaos a la funcion de conversión de imagen a un JSON
            datos = imagen_a_json(img)

            # Consumimos al endpoint /predict de Flask
            prediccion = requests.post(
                "http://127.0.0.1:5000/predict", 
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
                    "http://127.0.0.1:5000/predict_save", 
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

    if st.button("📄 Mostrar base de datos", width="stretch"):
        tabla = requests.get("http://127.0.0.1:5000/show_data_base")
        df = pd.DataFrame(tabla.json())

        st.dataframe(df[["id", "prediccion", "probabilidad", "fecha"]], width="stretch")

# Función que devuelve la BD por id (Conección por argumento) / Query
def mostrar_bd_id():
    st.subheader("🔎 Buscar predicción por ID 🔍")
    
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
    tabla = requests.get("http://127.0.0.1:5000/show_data_base")
    df = pd.DataFrame(tabla.json())    
    max_id = df["id"].max()

    id_buscar = st.number_input(
        "Ingrese el ID :", 
        min_value=1, 
        max_value=max_id,
        step=1,
    )
    st.caption("⚠️ Nota: Los IDs pueden no ser consecutivos si ya se han eliminado registros.")

    if st.button("Buscar Predicción"):
        respuesta = requests.get(f"http://127.0.0.1:5000/predict/{id_buscar}")
        
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
            st.error("‼️ Registro no encontrado, pruebe con otro")

# Borrar predicción por id (Conección por argumento)
def borrar_prediccion_id():
    st.subheader("🗑️ Borrar predicción por ID")
    st.markdown('<div class="tarjeta">', unsafe_allow_html=True)

    # Función auxiliar
    def cargar_bd():
        tabla = requests.get("http://127.0.0.1:5000/show_data_base")
        return pd.DataFrame(tabla.json())

    # Guardar BD en session_state para actualizar automaticamente
    if "df_bd" not in st.session_state:
        st.session_state["df_bd"] = cargar_bd()

    df = st.session_state["df_bd"]

    st.markdown("### 📂 Base de datos actual")
    st.dataframe(df[["id", "prediccion", "probabilidad", "fecha"]], use_container_width=True)
    
    if df.empty:
        st.warning("⚠️ La base de datos está vacía.")
    
    st.markdown("---")

    max_id = df["id"].max()

    id_borrar = st.number_input("ID a eliminar:", min_value=1, max_value=max_id, step=1)
    st.caption("⚠️ Nota: Los IDs pueden no ser consecutivos si ya se han eliminado registros.")


    if st.button("🗑️ Eliminar Predicción", type="primary"):
        respuesta = requests.delete(f"http://127.0.0.1:5000/delete_predict/{id_borrar}")

        if respuesta.status_code == 200:
            st.success("Predicción eliminada correctamente")
            st.session_state["df_bd"] = cargar_bd()  # recarga BD
            st.rerun()
        else:
            st.error("Error eliminando el registro")