import os
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

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

class_path = os.path.join(base_path, '..', 'modelado', 'clases.json')

with open(class_path, "r") as f:
    indices = json.load(f)

# Convertimos {clase → índice} a lista ordenada:
CLASES = [nombre for nombre, idx in sorted(indices.items(), key=lambda x: x[1])]

# -------------------------------
# 1) Página de inicio
# -------------------------------
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido"})

# -------------------------------
# 2) Hacer una predicción
# http://127.0.0.1:5000/predict
# -------------------------------
IMG_SIZE = (224, 224)
class_path = os.path.join(base_path, '..', 'modelado', 'clases.json')

with open(class_path, "r") as f:
    indices = json.load(f)

# Convertimos {clase → índice} a lista ordenada:
clases = [nombre for nombre, idx in sorted(indices.items(), key=lambda x: x[1])]

print("Clases detectadas:", clases)
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()   #  Se agrego get_json()

    if "imagen_base64" not in data:
        return jsonify({"error": "Falta el campo imagen_base64"}), 400

    # Decode Base64 → bytes
    imagen_bytes = base64.b64decode(data["imagen_base64"])
    imagen = Image.open(BytesIO(imagen_bytes)).convert("RGB")

    # Preprocesado igual que entrenamiento
    imagen = imagen.resize(IMG_SIZE)
    imagen = np.array(imagen).astype("float32")
    imagen = np.expand_dims(imagen, axis=0)  # (1, 224, 224, 3)

    # Predicción
    pred = model_importado.predict(imagen, verbose=0)[0]
    clase_idx = np.argmax(pred)
    clase_nombre = CLASES[clase_idx]

    return jsonify({
        "clase_nombre": clase_nombre,
        "probabilidades": pred.tolist(),
        "clase_idx": int(clase_idx)
    })

'''def predict():
    datos = request.json.get("valores")

    if not datos:
        return jsonify({"error": "Debes enviar una lista en 'valores'"}), 400

    arr = np.array([datos])
    pred = model.predict(arr)[0]

    return jsonify({
        "prediccion": str(pred),
        "clase_nombre": clases[pred] if pred < len(clases) else "desconocida"
    })'''


# -------------------------------
# 3) Probabilidad de incendio
# -------------------------------
@app.route("/fire_probability", methods=["POST"])
def fire_probability():

    data = request.get_json()

    if "imagen_base64" not in data:
        return jsonify({"error": "Falta el campo imagen_base64"}), 400

    # Decode Base64 → bytes
    imagen_bytes = base64.b64decode(data["imagen_base64"])
    imagen = Image.open(BytesIO(imagen_bytes)).convert("RGB")

    #Reducir tamaño, para analisis rapido

    img_small = imagen.resize((50, 50))
    arr = np.array(img_small)

    # Extraer canales
    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]

    #Determinar pixeles color marron

    brown_pixels = (R > 90) & (G < 50) & (B < 80)

    #Verde (vegetacion)
    green_pixels = (G > R) & (G > B)

    # Mide porcentaje dde verde y marron en la imagen
    total_pixels = arr.shape[0] * arr.shape[1]
    brown_count = np.sum(brown_pixels) / total_pixels
    green_count = np.sum(green_pixels) / total_pixels # píxeles marrones entre total de píxeles

    #Reglas del negocio
    if brown_count > 0.40:
        riesgo = "Alto"
    elif brown_count > 0.40:
        riesgo = "Medio"
    else:
        riesgo = "Bajo"

        return jsonify({
            "porcentaje_marron": float(brown_count),
            "porcentaje_verde": float(green_count),
            "nivel_riesgo_incendio": riesgo
        })

# -------------------------------
# 4) Monitoreo
# -------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "modelo_cargado": True,
        "clases_detectadas": len(CLASES)
    })

# -------------------------------
# 5) Información
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

        # Métricas del modelo / API
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
# Ejecutar app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)