

# Se crea la base de datos con SQLite pq es lo más facil

import sqlite3

conn = sqlite3.connect("predicciones.db")     # Esto es como la puerta para crear la base de datos, crear tablas y todo lo relacionado con esto
cursor = conn.cursor()      # Esto es como el tradutor que intermedia entre Python y el lenguaje SQL para ejecutar comandos SQL


# Esto es la tabla que se va a usar reciviendo los datos de API

cursor.execute('''
               
     CREATE TABLE IF NOT EXISTS prediccion(
               id INTEGER PRIMARY KEY AUTOINCREMENT,    
               prediccion TEXT,
               probabilidad REAL,
               date TEXT      
        );
''')

conn.commit() # guarda los cambios
conn.close()  # cierra la conexión 

print("Base de datos creada y actualizada correctamente")