from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# -------------------------------
# Cargar modelo
# -------------------------------
# Ruta absoluta del archivo actual
base_path = os.path.dirname(os.path.realpath(__file__))

# Construir la ruta al modelo dentro de la carpeta "modelos"
model_path = os.path.join(base_path, '..', 'modelado', 'modelo_final.keras')

# Cargar el modelo
model_importado = tf.keras.models.load_model(model_path)

clases = ["clase_0", "clase_1", "clase_2"]  # Cambiar a clases que usaremos
print(model_importado.summary())


# -------------------------------
# 1) Página de inicio
# -------------------------------
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido"})


# -------------------------------
# 2) Hacer una predicción
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    datos = request.json.get("valores")

    if not datos:
        return jsonify({"error": "Debes enviar una lista en 'valores'"}), 400

    arr = np.array([datos])
    pred = model_importado.predict(arr)[0]

    return jsonify({
        "prediccion": str(pred),
        "clase_nombre": clases[pred] if pred < len(clases) else "desconocida"
    })


# -------------------------------
# ) Comprobar si la API funciona
# -------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"estado": "ok"})


# -------------------------------
# ) Mostrar clases del modelo
# -------------------------------
@app.route("/classes", methods=["GET"])
def get_classes():
    return jsonify({"clases_del_modelo": clases})



# -------------------------------
# Ejecutar app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
