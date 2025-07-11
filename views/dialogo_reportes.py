from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from models.tarea import Tarea
from models.sprint import Sprint

class DialogoReportes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Reportes del Sprint Activo")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout(self)
        sprint = Sprint.obtener_activo()

        if not sprint:
            layout.addWidget(QLabel("No hay sprint activo."))
            return

        metricas = Tarea.obtener_metricas_sprint(sprint.id)

        # Evita errores si hay None
        total_tareas = metricas.get('total_tareas', 0) or 0
        tareas_completadas = metricas.get('tareas_completadas', 0) or 0
        total_points = metricas.get('total_points', 0) or 0
        points_completados = metricas.get('points_completados', 0) or 0
        progreso_tareas = metricas.get('progreso_tareas', 0.0)
        progreso_points = metricas.get('progreso_points', 0.0)

        layout.addWidget(QLabel(f"<b>Sprint:</b> {sprint.nombre}"))
        layout.addWidget(QLabel(f"<b>Objetivo:</b> {sprint.objetivo}"))
        layout.addWidget(QLabel(f"<b>Total Tareas:</b> {total_tareas}"))
        layout.addWidget(QLabel(f"<b>Tareas Completadas:</b> {tareas_completadas}"))
        layout.addWidget(QLabel(f"<b>Story Points:</b> {points_completados} / {total_points}"))
        layout.addWidget(QLabel(f"<b>Progreso Tareas:</b> {progreso_tareas}%"))
        layout.addWidget(QLabel(f"<b>Progreso Points:</b> {progreso_points}%"))
