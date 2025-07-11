import sqlite3
from datetime import date

class Sprint:
    @staticmethod
    def get_connection():
        return sqlite3.connect("agileflow.db")

    def __init__(self, id, nombre, objetivo=None, fecha_inicio=None, fecha_fin=None, estado="Planificado", velocidad_estimada=0):
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.velocidad_estimada = velocidad_estimada

    @staticmethod
    def obtener_activo():
        conn = Sprint.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints WHERE estado = 'Activo' ORDER BY fecha_inicio DESC LIMIT 1")
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return Sprint(*fila)
        return None

    @staticmethod
    def obtener_por_id(id):
        conn = Sprint.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints WHERE id = ?", (id,))
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return Sprint(*fila)
        return None

    @staticmethod
    def crear(nombre, objetivo, fecha_inicio: date, fecha_fin: date):
        conn = Sprint.get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE sprints SET estado = 'Finalizado' WHERE estado = 'Activo'")

        cursor.execute('''
            INSERT INTO sprints (nombre, objetivo, fecha_inicio, fecha_fin, estado)
            VALUES (?, ?, ?, ?, 'Activo')
        ''', (nombre, objetivo, fecha_inicio.isoformat(), fecha_fin.isoformat()))
        conn.commit()
        conn.close()

    @staticmethod
    def finalizar_sprint(id):
        conn = Sprint.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sprints SET estado = 'Finalizado' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
