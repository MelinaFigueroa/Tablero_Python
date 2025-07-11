# controllers/tarea_controller.py
from models.tarea import Tarea

def crear_tarea(data):
    return Tarea.crear(
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        tipo=data.get('tipo', 'Task'),
        prioridad=data.get('prioridad', 'Media'),
        estado=data.get('estado', 'To Do'),
        story_points=data.get('story_points', 0),
        asignado_a=data.get('asignado', ''),
        fecha_limite=data.get('fecha_limite'),
        criterios_aceptacion=data.get('criterios', ''),
        tags=data.get('tags', [])
    )

def actualizar_estado(tarea_id, nuevo_estado):
    return Tarea.cambiar_estado(tarea_id, nuevo_estado)

def obtener_tareas_por_estado(estado):
    return Tarea.obtener_por_estado(estado)

def eliminar_tarea(tarea_id: int) -> bool:
    tarea = Tarea.obtener_por_id(tarea_id)
    if tarea:
        return tarea.eliminar()
    return False

def actualizar_tarea(tarea_id: int, datos: dict) -> bool:
    tarea = Tarea.obtener_por_id(tarea_id)
    if tarea:
        return tarea.actualizar(**datos)
    return False
