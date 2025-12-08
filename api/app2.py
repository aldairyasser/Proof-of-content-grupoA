import os
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
import json
from flask import Flask, request, jsonify
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data-base'))
import mi_bd

app = Flask(__name__) # Crea la aplicación web Flask donde estarán todas las rutas.

# -------------------------------
# Cargar modelo
# -------------------------------
# Ruta absoluta del archivo actual
base_path = os.path.dirname(os.path.realpath(__file__))

# Construir la ruta al modelo dentro de la carpeta "modelos"
model_path = os.path.join(base_path, '..','modelado', 'modelo_final.keras')

# Cargar el modelo
model_importado = tf.keras.models.load_model(model_path)

# -------------------------------
# Leemos las clases
# -------------------------------

# Ruta del archivo que contiene los nombres de las clases
class_path = os.path.join(base_path, '..', 'modelado', 'clases.json')

# Abre el archivo y carga su contenido
with open(class_path, "r") as f:
    indices = json.load(f)

# Convertimos {clase → índice} a lista ordenada:
CLASES = [nombre for nombre, idx in sorted(indices.items(), key=lambda x: x[1])]

# -------------------------------
# 1) Página de inicio
# -------------------------------

# Ruta principal que solo muestra un mensaje de bienvenida
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido"})

# -------------------------------
# 2) Hacer una predicción
# http://127.0.0.1:5000/predict
# -------------------------------

# Tamaño al que se ajustarán las imágenes
IMG_SIZE = (224, 224)
class_path = os.path.join(base_path, '..', 'modelado', 'clases.json') # Vuelve a leer las clases (repetido pero funcional)

with open(class_path, "r") as f:
    indices = json.load(f)

# Convertimos {clase → índice} a lista ordenada:
clases = [nombre for nombre, idx in sorted(indices.items(), key=lambda x: x[1])]

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()   # # Recibe los datos enviados en formato JSON

    if "imagen_base64" not in data:
        return jsonify({"error": "Falta el campo imagen_base64"}), 400 # Verifica que se haya enviado la imagen

    # Convierte el texto Base64 en bytes y luego en imagen
    imagen_bytes = base64.b64decode(data["imagen_base64"])
    imagen = Image.open(BytesIO(imagen_bytes)).convert("RGB")

    #Ajusta tamaño igual que en el entrenamiento
    imagen = imagen.resize(IMG_SIZE)
    imagen = np.array(imagen).astype("float32")
    imagen = np.expand_dims(imagen, axis=0)  # (1, 224, 224, 3)

    # Predicción
    pred = model_importado.predict(imagen, verbose=0)[0]
    predict_proba = pred.tolist() # % de todas la clases  # Convierte la predicción a lista
    acc = round(float(np.max(pred))*100, 2) # Obtiene la probabilidad más alta

    # Obtiene qué clase fue la ganadora
    clase_idx = np.argmax(pred)
    clase_nombre = CLASES[clase_idx]

    return jsonify({
        "clase_nombre": clase_nombre,  # Devuelve la clase y su probabilidad
        "probabilidades": acc
    })

# -------------------------------
# 3) Envio de predicción y guardado en BD
# -------------------------------

@app.route("/predict_save", methods=["POST"])
def predic_save():
        
        mi_bd.inicia_bd()

        data = request.get_json()   # Toma los datos enviados

        # Obtiene los valores enviados
        nombre = data["clase_nombre"]
        acc = data["probabilidades"]

        # Guardar en BD
        id_prediccion = mi_bd.mete_prediccion(nombre, acc)

        return jsonify({"El id": id_prediccion})   # Devuelve el ID creado

# -------------------------------
# 4) Mostrar base de datos
# -------------------------------

#Obtiene todas las filas de la tabla y las envía como JSON
@app.route("/show_data_base", methods=["GET"])
def showdatabase():
    registros = mi_bd.full_tabla()
    return jsonify(registros)

# -------------------------------
# 5) Predicción por ID (FUTURA MEJORA LINK DE LA IMÁGEN)
# -------------------------------

@app.route('/prediccion/<int:id>', methods=['GET']) 
def obtener_prediccion(id):
    try: 
        # Busca un registro por su ID
        fila = mi_bd.search_id(id)

        if fila is None:  # Si no existe, responde error
            return jsonify({"error": "Predicción no encontrada"}), 404
        
        # Si existe, la devuelve
        return jsonify(fila) 
    
    except Exception as e:
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500  

# -------------------------------
# 6) Probabilidad de incendio
# -------------------------------
@app.route("/fire_probability", methods=["POST"])
def fire_probability():

    # Toma datos JSON
    data = request.get_json()

    # Verifica que exista imagen
    if "imagen_base64" not in data:
        return jsonify({"error": "Falta el campo imagen_base64"}), 400

     # Convierte Base64 a imagen
    imagen_bytes = base64.b64decode(data["imagen_base64"])
    imagen = Image.open(BytesIO(imagen_bytes)).convert("RGB")

    #Reducir tamaño, para analisis rapido
    img_small = imagen.resize((50, 50))
    arr = np.array(img_small)

    # Separa los colores
    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]

    # Determinar pixeles color marron
    brown_pixels = (R > 90) & (G < 50) & (B < 80)

    # Detecta zonas verdes (vegetación)
    green_pixels = (G > R) & (G > B)

    # Mide porcentaje dde verde y marron en la imagen
    total_pixels = arr.shape[0] * arr.shape[1]
    brown_count = np.sum(brown_pixels) / total_pixels # píxeles marrones entre total de píxeles
    green_count = np.sum(green_pixels) / total_pixels # píxeles verdes entre total de píxeles

    # # Reglas simples para determinar riesgo
    if brown_count > 0.40:
        riesgo = "Alto"
    elif brown_count > 0.40:
        riesgo = "Medio"
    else:
        riesgo = "Bajo"

         # Devuelve resultados
        return jsonify({
            "porcentaje_marron": float(brown_count),
            "porcentaje_verde": float(green_count),
            "nivel_riesgo_incendio": riesgo
        })

# -------------------------------
# 7) Monitoreo
# -------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "modelo_cargado": True,
        "clases_detectadas": len(CLASES)
    })
    # Sirve para saber si el servidor y el modelo están funcionando.

# -------------------------------
# 8) Información
# -------------------------------
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "status": "ok",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        # Resumen de funcionalidades disponibles en la API
        "features": [
            "Clasificación de imágenes mediante modelo TensorFlow",
            "Análisis de riesgo de incendio basado en colores",
            "Monitoreo del estado del servidor",
            "Procesamiento de imágenes en Base64"
        ],

        # Datos generales del sistema
        "metrica": {
            "version_api": "1.0.0",
            "version_modelo": "1.0.0",
            "framework": "TensorFlow",
            "input_size": list(IMG_SIZE),
            "cantidad_clases": len(CLASES),
            "formato_entrada": "Base64 / JSON"
        }
    })

# -------------------------------
# 9) Listar todas las predicciones
# -------------------------------

@app.route("/predicciones", methods=["GET"])
def obtener_predicciones():
    try:
        # Abre la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta todas las filas de la tabla prediccion
        cursor.execute("SELECT * FROM prediccion")
        filas = cursor.fetchall()
        conn.close()

        # Convierte los registros en lista de diccionarios
        lista = []
        for fila in filas:
            lista.append({
                "id": fila["id"],
                "prediccion": fila["prediccion"],
                "probabilidad": fila["probabilidad"],
                "date": fila["date"]
            })

        return jsonify(lista)

    except Exception as e:
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500
# -------------------------------
# Ejecutar app
# -------------------------------

#Inicia el servidor Flask cuando se ejecuta el archivo.
if __name__ == "__main__":
    app.run(debug=True)