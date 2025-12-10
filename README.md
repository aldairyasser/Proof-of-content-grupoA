# Proof-of-content-grupoA

# 🚀 Sistema de Detección de Riesgo de Incendio a partir de Imágenes Satelitales

Este proyecto implementa un sistema capaz de analizar imágenes satelitales, detectar vegetación, tierra seca y estimar el riesgo de incendio. Incluye una API desarrollada con Flask y una interfaz gráfica creada con Streamlit para interactuar fácilmente con el modelo.

---

## 📌 Características principales

- **API REST con Flask**
  - Analiza imágenes enviadas en Base64.
  - Calcula porcentaje de verde (vegetación).
  - Calcula porcentaje de marrón (suelo seco o árido).
  - Estima nivel de riesgo de incendio.
  - Permite almacenar, consultar y borrar registros en la base de datos.

- **Detección robusta basada en colores**
  - Análisis RGB + HSV.
  - Más precisa para imágenes satelitales.
  - Mejora la detección de zonas áridas.

- **Interfaz en Streamlit**
  - Subida de imágenes.
  - Visualización de resultados.
  - Consulta y borrado de elementos de la base de datos.
  - Botón de refresco que no reinicia la navegación.
  - Textos justificados y estilizados.

---

## 📁 Estructura del proyecto

📦 proyecto-incendios
┣ 📂 backend
┃ ┣ app.py
┃ ┣ utils.py
┃ ┣ requirements.txt
┃ ┗ models/
┣ 📂 frontend
┃ ┣ front_streamlit.py
┃ ┣ funtion.py
┃ ┗ styles.css
┣ README.md

yaml
Copiar código

---

## 🔧 Tecnologías utilizadas

- Python 3.10+
- Flask (API REST)
- Streamlit (Frontend)
- Numpy
- Pandas
- Pillow (procesamiento de imágenes)
- SQLite (base de datos)
- Requests

---

## ▶️ Cómo ejecutar el proyecto

### 1️⃣ Instalar dependencias

En el backend:

```bash
pip install -r backend/requirements.txt
En el frontend:

bash
Copiar código
pip install streamlit requests pandas pillow numpy
2️⃣ Ejecutar el servidor Flask
Desde la carpeta backend:

bash
Copiar código
python app.py
3️⃣ Ejecutar la interfaz Streamlit
Desde la carpeta frontend:

bash
Copiar código
streamlit run front_streamlit.py
🔥 Endpoint principal: /fire_probability
✔️ Método: POST
✔️ Body (JSON)
json
Copiar código
{
  "imagen_base64": "<string_base64>"
}
✔️ Respuesta
json
Copiar código
{
  "porcentaje_marron": 0.12,
  "porcentaje_verde": 0.53,
  "nivel_riesgo_incendio": "Medio"
}
🗄️ Base de datos
El proyecto utiliza SQLite y genera automáticamente la tabla:

sql
Copiar código
CREATE TABLE IF NOT EXISTS predicciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediccion TEXT,
    probabilidad FLOAT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Incluye endpoints para:

Ver base completa → /show_data_base

Consultar por ID → /prediccion_query

Borrar por ID → /borrar_prediccion/<id>

📸 Interfaz Streamlit
La aplicación incluye:

Carga de imágenes.

Vista del análisis recibido desde Flask.

Búsqueda y borrado de predicciones por ID.

Vista de la base de datos completa.

Botón de refresco que no te envía al Home.

📌 Mejoras futuras
Entrenamiento de un modelo ML para crear una clasificación más compleja.

Uso de Google Earth Engine para obtener imágenes automáticamente.

Añadir exportación de reportes PDF/CSV.

