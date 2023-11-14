import pandas as pd
import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_name = 'database.db'
        self.crear_tabla_contador('Contador')

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def agregarDs(self):
        fecha_actual = datetime.now()
        fecha = fecha_actual.strftime('%d-%m-%Y')
        hora = fecha_actual.strftime('%H:%M')
        query = 'INSERT INTO Contador VALUES(NULL, ?, ?)'
        parametros = (fecha, hora)
        self.run_query(query, parametros)

    def conteo_diario(self):
        fecha_actual = datetime.now()
        fecha = fecha_actual.strftime('%d-%m-%Y')
        query = "SELECT COUNT(*) AS conteo_diario FROM Contador WHERE fecha = ?"
        parametros = (fecha,)
        result = self.run_query(query, parametros)
        conteo = result.fetchone()[0]
        return conteo

    def Obtener_registros(self):
        query = "SELECT * FROM Contador ORDER BY fecha ASC"
        db_rows = self.run_query(query)
        return db_rows

    def descargar_registros(self):
        query = "SELECT * FROM Contador"
        db_connection = sqlite3.connect(self.db_name)
        df = pd.read_sql(query, db_connection)
        download_folder = os.path.expanduser("~")
        download_path = os.path.join(download_folder, "Downloads")
        output_file = os.path.join(download_path, 'registro_ds.xlsx')
        df.to_excel(output_file,index=False, engine='openpyxl', if_exists='replace')

    def Eliminar_registro_diario(self):
        fecha_actual = datetime.now()
        fecha = fecha_actual.strftime('%d-%m-%Y')
        query = 'DELETE FROM Contador WHERE fecha = ?'
        parametros = (fecha,)
        self.run_query(query, parametros)

    def crear_tabla_contador(self, tabla):
        query = """CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )""".format(tabla)
        self.run_query(query)

    def crear_tabla_usuarios(self, tabla):
        query = """CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL""".format(tabla)
        self.run_query(query)

    def insertar_usuario(self, nombre, apellido, email, telefono):
        query = """INSERT INTO Usuarios (nombre, apellido, email, telefono) VALUES (?, ?, ?, ?)"""
        parametros = (nombre, apellido, email, telefono)
        self.run_query(query, parametros)

    def insertar_registro(self, fecha, hora):
        query = """INSERT INTO Contador (fecha, hora) VALUES (?, ?)"""
        parametros = (fecha, hora)
        self.run_query(query, parametros)

    def obtener_usuarios(self):
        query = """SELECT * FROM Usuarios"""
        db_rows = self.run_query(query)
        return db_rows

    