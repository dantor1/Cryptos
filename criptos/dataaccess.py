import sqlite3
from criptos import app

DATABASE = app.config['DATABASE']


def consultaSQL (query, parametros=()):
    # Abrimos la conexión
    conexion = sqlite3.connect(DATABASE)
    cur = conexion.cursor()
    
    # Ejecutamos la consulta
    cur.execute(query, parametros)
    conexion.commit()
    
    filas = cur.fetchall()
    
    # Procesamos los datos
    if len(filas) == 0:
        return filas
    else:
        pass

    cabeceras = list()
    for una_cabecera in cur.description:
        cabeceras.append(una_cabecera[0])

    resultado = list()
    for fila in filas:
        d={}
        for i, una_cabecera in enumerate(cabeceras):
            d[una_cabecera]= fila[i]
        resultado.append(d)

    # Cerramos la conexión
    conexion.close()

    return resultado