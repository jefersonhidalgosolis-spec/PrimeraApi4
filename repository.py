from pydantic import BaseModel
from typing import Optional, List

import pyodbc

class ProductoRepository:
    def __init__(self):
        # Asegúrate de que el nombre del SERVER sea el correcto
        self.conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-6ID37KR;'
            'DATABASE=MiProyectoDB;'
            'Trusted_Connection=yes;'
        )

    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    #listar_productos
    #recibe la peticion y empieza a comunicarse con la base de datos mediante consultas para obtener los datos. 
    #Se encarga de abrir la conexión, ejecutar la consulta SQL para extraer los registros de la tabla 'Productos' 
    #y transformar los resultados en una estructura de datos compatible con la lógica del negocio.
    def obtener_todos(self):
        conn = self._get_connection() #abrir conexion con la BD 
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM Productos") #ejecutar la consulta SQL para extraer los registros de la tabla 'Productos'
        productos = []
        for row in cursor.fetchall(): #estructura de datos compatibles en formato JSON 
            productos.append({
                "id": row[0],
                "nombre": row[1],
                "precio": float(row[2]),
                "stock": row[3]
            })
        conn.close() #cierra conexion 
        return productos 

    #buscar_por_id 
    #  
    def obtener_por_id(self, p_id: int):
        conn = self._get_connection()#abrir conexion con la BD 
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM Productos WHERE id = ?", (p_id,)) #ejecutar la consulta SQL para extraer los registros de un id especifico de la tabla 'Productos'
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "nombre": row[1], "precio": float(row[2]), "stock": row[3]}#estructura de datos compatibles en formato JSON 
            conn.close()#cierra conexion 
        return None

    #crear_nuevo
    def guardar(self, nombre, precio, stock):
        conn = self._get_connection()#abrir conexion con la BD 
        cursor = conn.cursor()
        query = "INSERT INTO Productos (nombre, precio, stock) VALUES (?, ?, ?)"
        cursor.execute(query, (nombre, precio, stock))
        conn.commit()
        conn.close()
        return {"mensaje": "Creado correctamente"}

    #actualizar_producto
    def actualizar(self, p_id, nombre, precio, stock):
        conn = self._get_connection()#abrir conexion con la BD 
        cursor = conn.cursor()
        query = "UPDATE Productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?"
        cursor.execute(query, (nombre, precio, stock, p_id))
        conn.commit()
        filas = cursor.rowcount
        conn.close()
        return filas > 0

    #borrar
    def eliminar(self, p_id: int):
        conn = self._get_connection()#abrir conexion con la BD 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = ?", (p_id,))
        conn.commit()
        filas = cursor.rowcount
        conn.close()
        return filas > 0