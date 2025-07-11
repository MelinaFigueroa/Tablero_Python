import sqlite3
from database.db import get_connection
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class PrioridadTarea(Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"

class TipoTarea(Enum):
    USER_STORY = "User Story"
    BUG = "Bug"
    TASK = "Task"
    EPIC = "Epic"
    SPIKE = "Spike"

class EstadoTarea(Enum):
    BACKLOG = "Backlog"
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    REVIEW = "Code Review"
    TESTING = "Testing"
    DONE = "Done"

@dataclass
class Tarea:
    id: Optional[int] = None
    titulo: str = ""
    descripcion: str = ""
    tipo: str = TipoTarea.USER_STORY.value
    prioridad: str = PrioridadTarea.MEDIA.value
    estado: str = EstadoTarea.TODO.value
    story_points: int = 0
    asignado_a: str = ""
    fecha_creacion: datetime = None
    fecha_limite: Optional[date] = None
    fecha_completado: Optional[datetime] = None
    criterios_aceptacion: str = ""
    tags: List[str] = None
    tiempo_estimado: int = 0
    tiempo_real: int = 0
    sprint_id: Optional[int] = None
    epic_id: Optional[int] = None

    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()
        if self.tags is None:
            self.tags = []

    @classmethod
    def crear(cls, titulo: str, descripcion: str = "", **kwargs) -> 'Tarea':
        if not titulo.strip():
            raise ValueError("El título de la tarea no puede estar vacío")

        tarea = cls(titulo=titulo.strip(), descripcion=descripcion.strip(), **kwargs)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tareas (
                        titulo, descripcion, tipo, prioridad, estado,
                        story_points, asignado_a, fecha_creacion, fecha_limite,
                        criterios_aceptacion, tags, tiempo_estimado, sprint_id, epic_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tarea.titulo, tarea.descripcion, tarea.tipo, tarea.prioridad,
                    tarea.estado, tarea.story_points, tarea.asignado_a,
                    tarea.fecha_creacion.isoformat(),
                    tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
                    tarea.criterios_aceptacion, ','.join(tarea.tags),
                    tarea.tiempo_estimado, tarea.sprint_id, tarea.epic_id
                ))
                tarea.id = cursor.lastrowid
                conn.commit()
                return tarea
        except sqlite3.Error as e:
            raise Exception(f"Error creando tarea: {e}")

    @classmethod
    def obtener_por_id(cls, tarea_id: int) -> Optional['Tarea']:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tareas WHERE id = ?', (tarea_id,))
                row = cursor.fetchone()
                if row:
                    return cls._from_db_row(row)
                return None
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo tarea: {e}")

    @classmethod
    def obtener_por_estado(cls, estado: str) -> List['Tarea']:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM tareas WHERE estado = ? ORDER BY prioridad DESC, fecha_creacion ASC',
                    (estado,)
                )
                return [cls._from_db_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo tareas por estado: {e}")

    @classmethod
    def obtener_por_sprint(cls, sprint_id: int) -> List['Tarea']:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM tareas WHERE sprint_id = ? ORDER BY estado, prioridad DESC',
                    (sprint_id,)
                )
                return [cls._from_db_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo tareas por sprint: {e}")

    @classmethod
    def obtener_por_asignado(cls, asignado: str) -> List['Tarea']:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM tareas WHERE asignado_a = ? ORDER BY prioridad DESC, fecha_limite ASC',
                    (asignado,)
                )
                return [cls._from_db_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo tareas por asignado: {e}")

    @staticmethod
    def cambiar_estado(tarea_id, nuevo_estado):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE tareas SET estado = ?, fecha_completado = datetime('now') WHERE id = ?",
                    (nuevo_estado, tarea_id)
                )
                conn.commit()
                return True
        except Exception as e:
            raise Exception(f"Error cambiando estado de tarea: {e}")

    def actualizar(self, **kwargs) -> bool:
        if not self.id:
            raise ValueError("No se puede actualizar una tarea sin ID")

        campos_actualizar = []
        valores = []

        for campo, valor in kwargs.items():
            if hasattr(self, campo):
                campos_actualizar.append(f"{campo} = ?")
                valores.append(valor)
                setattr(self, campo, valor)

        if not campos_actualizar:
            return False

        valores.append(self.id)
        query = f"UPDATE tareas SET {', '.join(campos_actualizar)} WHERE id = ?"

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, valores)
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error actualizando tarea: {e}")

    def eliminar(self) -> bool:
        if not self.id:
            raise ValueError("No se puede eliminar una tarea sin ID")

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM tareas WHERE id = ?', (self.id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error eliminando tarea: {e}")

    @classmethod
    def obtener_metricas_sprint(cls, sprint_id: int) -> Dict[str, Any]:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_tareas,
                        SUM(story_points) as total_points,
                        SUM(CASE WHEN estado = 'Done' THEN story_points ELSE 0 END),
                        COUNT(CASE WHEN estado = 'Done' THEN 1 END)
                    FROM tareas 
                    WHERE sprint_id = ?
                ''', (sprint_id,))
                row = cursor.fetchone()
                if row:
                    total_tareas, total_points, points_completados, tareas_completadas = row
                    return {
                        'total_tareas': total_tareas or 0,
                        'tareas_completadas': tareas_completadas or 0,
                        'total_points': total_points or 0,
                        'points_completados': points_completados or 0,
                        'progreso_tareas': round((tareas_completadas / total_tareas * 100) if total_tareas else 0, 1),
                        'progreso_points': round((points_completados / total_points * 100) if total_points else 0, 1)
                    }
                return {}
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo métricas: {e}")

    @classmethod
    def obtener_burndown_chart_data(cls, sprint_id: int) -> Dict[str, List]:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT DATE(fecha_completado), SUM(story_points)
                    FROM tareas 
                    WHERE sprint_id = ? AND estado = 'Done' AND fecha_completado IS NOT NULL
                    GROUP BY DATE(fecha_completado)
                    ORDER BY fecha
                ''', (sprint_id,))
                rows = cursor.fetchall()
                fechas, points_acumulados = [], []
                total = 0
                for fecha, puntos in rows:
                    fechas.append(fecha)
                    total += puntos
                    points_acumulados.append(total)
                return {'fechas': fechas, 'points_completados': points_acumulados}
        except sqlite3.Error as e:
            raise Exception(f"Error obteniendo datos burndown: {e}")

    @classmethod
    def _from_db_row(cls, row) -> 'Tarea':
        return cls(
            id=row[0],
            titulo=row[1],
            descripcion=row[2],
            tipo=row[3],
            prioridad=row[4],
            estado=row[5],
            story_points=row[6],
            asignado_a=row[7],
            fecha_creacion=datetime.fromisoformat(row[8]) if row[8] else None,
            fecha_limite=date.fromisoformat(row[9]) if row[9] else None,
            fecha_completado=datetime.fromisoformat(row[10]) if row[10] else None,
            criterios_aceptacion=row[11] or "",
            tags=row[12].split(',') if row[12] else [],
            tiempo_estimado=row[13] or 0,
            tiempo_real=row[14] or 0,
            sprint_id=row[15],
            epic_id=row[16]
        )

    def __str__(self):
        return f"Tarea(id={self.id}, titulo='{self.titulo}', estado='{self.estado}')"

    def __repr__(self):
        return self.__str__()
