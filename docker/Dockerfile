# 1) Imagen base con versión compatible con TensorFlow
FROM python:3.10-slim

# 2) Evita archivos .pyc y salida con buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3) Carpeta dentro del contenedor
WORKDIR /app

# 4) Instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copiar TODO el proyecto
COPY . /app

# 6) Exponer el puerto interno de la API
EXPOSE 5001

# 7) Ejecutar la API real -> app2.py
CMD ["gunicorn", "api.app2:app", "--bind", "0.0.0.0:5001"]
