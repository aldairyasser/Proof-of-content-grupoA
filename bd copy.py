

# Se crea la base de datos con SQLite pq es lo más facil

import sqlite3
from sqlite3 import Connection
from pathlib import Path 


BD_PATH = Path("predicciones.db")


# Con esto se abre la conexion a la BBDD

def pedir_conexion():
    
    conn = sqlite3.connect(BD_PATH)     # Esto es como la puerta para crear la base de datos, crear tablas y todo lo relacionado con esto
    conn.row_factory = sqlite3.Row        # como SQL devuelve tuplas, con esto se cambia el formato a diccionario
    return conn




# Esto es la tabla que se va a usar reciviendo los datos de API

def inicia_bd():
    
    conn = pedir_conexion()
    cursor = conn.cursor()    # Esto es como el tradutor que intermedia entre Python y el lenguaje SQL para ejecutar comandos SQL

    cursor.execute('''
               
    CREATE TABLE IF NOT EXISTS predicciones(
               id INTEGER PRIMARY KEY AUTOINCREMENT,    
               prediccion TEXT,
               probabilidad REAL,
               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP      
             );
     ''')

    conn.commit() # guarda los cambios
    conn.close()  # cierra la conexión 



# inserta la predicciony la probabilidad y las mete en la tabla para poder luego consultarlas

def mete_prediccion(prediccion: str,probabilidad: float):
    
    conn = pedir_conexion()
    cursor = conn.cursor()

    cursor.execute('''

        INSERT INTO predicciones (prediccion, probabilidad)
        VALUES (?, ?);           
                   
                   ''', (prediccion,probabilidad))  # esta última linea va a sustituir a ? ? , se hace para que meta los valores automaticamente pyhton
    
    conn.commit()
    prediccion_id = cursor.lastrowid
    conn.close()

    return prediccion_id


# esta función devuelve todo el registro de la base de datos
def full_tabla():
    
    conn = pedir_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute('''

                SELECT id, prediccion, probabilidad, date FROM predicciones;
                   
                   ''')
    
        filas = cursor.fetchall()  # devuelve todos los registros

        

        return [dict(r) for r in filas]  # devuelve un diccionario
    
    finally:
        conn.close()