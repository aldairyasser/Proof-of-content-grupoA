import base64
import mimetypes
from io import BytesIO
from PIL import Image


def imagen_a_json(imagen):

    buffer = BytesIO()
    imagen.save(buffer, format="JPEG")
    imagen_bytes = buffer.getvalue()

    imagen_codificada = base64.b64encode(imagen_bytes).decode("utf-8")

    return {
        "imagen_base64": imagen_codificada
    }


'''def imagen_a_json(imagen):
    """
    Convierte una imagen (objeto bytes o UploadedFile) a JSON con Base64.
    archivo_imagen: puede ser bytes, Streamlit UploadedFile, o un buffer tipo BytesIO.
    """
    try:
        # Obtener nombre si existe
        nombre = getattr(imagen, "name", "imagen_sin_nombre")

        # Detectar MIME por nombre
        tipo_archivo, _ = mimetypes.guess_type(nombre)
        if tipo_archivo is None:
            tipo_archivo = "application/octet-stream"

        # Obtener bytes dependiendo del tipo
        if isinstance(imagen, Image.Image):
            # Convertir PIL → bytes
            buffer = BytesIO()
            imagen.save(buffer, format=imagen.format or "PNG")
            imagen_bytes = buffer.getvalue()

        elif hasattr(imagen, "read"):
            # UploadedFile / BytesIO
            imagen_bytes = imagen.read()

        elif isinstance(imagen, bytes):
            imagen_bytes = imagen

        else:
            raise TypeError("Tipo de objeto no soportado para conversión a Base64.")

        # Codificar a Base64
        imagen_codificada = base64.b64encode(imagen_bytes).decode("utf-8")

        return {
            "nombre_archivo": nombre,
            "tipo_archivo": tipo_archivo,
            "datos_base64": imagen_codificada
        }

    except Exception as e:
        raise Exception(f"Error procesando imagen: {e}")'''