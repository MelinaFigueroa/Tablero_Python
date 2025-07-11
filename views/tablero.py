from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QScrollArea,
    QDialog, QLineEdit, QTextEdit, QFormLayout, QDialogButtonBox, QComboBox,
    QSpinBox, QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QDate
from controllers.tarea_controller import crear_tarea, actualizar_estado, obtener_tareas_por_estado
from views.tarjeta import Tarjeta
from views.columna import ColumnaKanban
from models.tarea import Tarea
from enum import Enum
from views.dialogo_sprint import DialogoSprint
from views.dialogo_reportes import DialogoReportes
from models.sprint import Sprint
from datetime import date


class EstadosTarea(Enum):
    BACKLOG = "Backlog"
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    REVIEW = "Code Review"
    TESTING = "Testing"
    DONE = "Done"


class DialogoTarea(QDialog):
    def __init__(self, tarea=None, parent=None):
        super().__init__(parent)
        self.tarea = tarea
        self.setWindowTitle("Nueva Tarea" if not tarea else "Editar Tarea")
        self.setFixedSize(500, 600)
        self.setupUI()
        if tarea:
            self.cargar_datos_tarea()

    def setupUI(self):
        layout = QFormLayout(self)

        self.titulo_edit = QLineEdit()
        self.titulo_edit.setPlaceholderText("Título de la tarea...")
        layout.addRow("Título*:", self.titulo_edit)

        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setPlaceholderText("Como [usuario], quiero [funcionalidad] para [beneficio]...")
        self.descripcion_edit.setMaximumHeight(100)
        layout.addRow("Historia de Usuario:", self.descripcion_edit)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["User Story", "Bug", "Task", "Epic", "Spike"])
        layout.addRow("Tipo:", self.tipo_combo)

        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(["Baja", "Media", "Alta", "Crítica"])
        layout.addRow("Prioridad:", self.prioridad_combo)

        self.story_points_spin = QSpinBox()
        self.story_points_spin.setRange(1, 100)
        self.story_points_spin.setValue(3)
        layout.addRow("Story Points:", self.story_points_spin)

        self.asignado_edit = QLineEdit()
        self.asignado_edit.setPlaceholderText("Nombre del desarrollador...")
        layout.addRow("Asignado a:", self.asignado_edit)

        self.fecha_limite = QDateEdit()
        self.fecha_limite.setDate(QDate.currentDate().addDays(7))
        self.fecha_limite.setCalendarPopup(True)
        layout.addRow("Fecha Límite:", self.fecha_limite)

        self.criterios_edit = QTextEdit()
        self.criterios_edit.setPlaceholderText("- Dado que...\n- Cuando...\n- Entonces...")
        self.criterios_edit.setMaximumHeight(80)
        layout.addRow("Criterios de Aceptación:", self.criterios_edit)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("frontend, api, database (separados por comas)")
        layout.addRow("Tags:", self.tags_edit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

    def accept(self):
        if not self.titulo_edit.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "El título no puede estar vacío.")
            return
        if self.fecha_limite.date().toPyDate() < date.today():
            QMessageBox.warning(self, "Fecha inválida", "La fecha límite no puede ser anterior a hoy.")
            return
        super().accept()

    def cargar_datos_tarea(self):
        self.titulo_edit.setText(self.tarea.titulo)
        self.descripcion_edit.setText(self.tarea.descripcion or "")

    def obtener_datos(self):
        return {
            'titulo': self.titulo_edit.text().strip(),
            'descripcion': self.descripcion_edit.toPlainText().strip(),
            'tipo': self.tipo_combo.currentText(),
            'prioridad': self.prioridad_combo.currentText(),
            'story_points': self.story_points_spin.value(),
            'asignado': self.asignado_edit.text().strip(),
            'fecha_limite': self.fecha_limite.date().toPyDate(),
            'criterios': self.criterios_edit.toPlainText().strip(),
            'tags': [tag.strip() for tag in self.tags_edit.text().split(',') if tag.strip()]
        }


class TableroKanban(QWidget):
    def __init__(self):
        super().__init__()
        self.columnas = {}
        self.auto_refresh_timer = QTimer()
        self.setupUI()
        self.recargar()
        self.auto_refresh_timer.timeout.connect(self.recargar)
        self.auto_refresh_timer.start(30000)

    def setupUI(self):
        self.setWindowTitle("AgileFlow - Kanban Scrum Board")
        self.setGeometry(100, 100, 1400, 800)

        try:
            with open("views/estilos.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilos no encontrado.")

        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(15)

        toolbar = self.crear_toolbar()
        layout_principal.addWidget(toolbar)

        scroll_horizontal = QScrollArea()
        scroll_horizontal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_horizontal.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_horizontal.setWidgetResizable(True)

        columnas_widget = QWidget()
        self.layout_columnas = QHBoxLayout(columnas_widget)
        self.layout_columnas.setSpacing(15)
        self.layout_columnas.setContentsMargins(10, 10, 10, 10)

        scroll_horizontal.setWidget(columnas_widget)
        layout_principal.addWidget(scroll_horizontal)

    def crear_toolbar(self):
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar_layout = QHBoxLayout(toolbar)

        btn_nueva_tarea = QPushButton("➕ Nueva Tarea")
        btn_nueva_tarea.setObjectName("btn-primary")
        btn_nueva_tarea.clicked.connect(self.crear_tarea)

        btn_refresh = QPushButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.recargar)

        btn_sprint = QPushButton("🏃 Gestionar Sprint")
        btn_sprint.clicked.connect(self.gestionar_sprint)

        btn_reportes = QPushButton("📊 Reportes")
        btn_reportes.clicked.connect(self.mostrar_reportes)

        self.filtro_asignado = QComboBox()
        self.filtro_asignado.addItem("Todos los usuarios")
        self.filtro_asignado.currentTextChanged.connect(self.aplicar_filtros)

        self.filtro_prioridad = QComboBox()
        self.filtro_prioridad.addItems(["Todas las prioridades", "Crítica", "Alta", "Media", "Baja"])
        self.filtro_prioridad.currentTextChanged.connect(self.aplicar_filtros)

        toolbar_layout.addWidget(btn_nueva_tarea)
        toolbar_layout.addWidget(btn_refresh)
        toolbar_layout.addWidget(btn_sprint)
        toolbar_layout.addWidget(btn_reportes)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(QLabel("Filtrar por:"))
        toolbar_layout.addWidget(self.filtro_asignado)
        toolbar_layout.addWidget(self.filtro_prioridad)

        return toolbar

    def recargar(self):
        for columna in self.columnas.values():
            columna.limpiar()

        if not self.columnas:
            self.crear_columnas()

        self.cargar_tareas()

    def crear_columnas(self):
        for estado in EstadosTarea:
            columna = ColumnaKanban(estado)
            columna.tarea_movida.connect(self.mover_tarea)
            self.columnas[estado] = columna
            self.layout_columnas.addWidget(columna)

    def cargar_tareas(self):
        try:
            usuarios = set()
            for estado in EstadosTarea:
                tareas = obtener_tareas_por_estado(estado.value)
                for tarea in tareas:
                    usuarios.add(tarea.asignado_a)

                    if self.filtro_asignado.currentText() != "Todos los usuarios" and tarea.asignado_a != self.filtro_asignado.currentText():
                        continue
                    if self.filtro_prioridad.currentText() != "Todas las prioridades" and tarea.prioridad != self.filtro_prioridad.currentText():
                        continue

                    tarjeta = Tarjeta(
                        tarea.id, tarea.titulo, tarea.descripcion, tarea.tipo,
                        tarea.prioridad, tarea.asignado_a, tarea.story_points, tarea.tags
                    )
                    tarjeta.editada.connect(self.editar_tarea)
                    tarjeta.eliminada.connect(self.eliminar_tarea)
                    tarjeta.reportada.connect(self.mostrar_reporte_tarea)  # ✅ nueva conexión
                    self.columnas[estado].agregar_tarjeta(tarjeta)

            self.actualizar_filtro_usuarios(usuarios)
        except Exception as e:
            print(f"Error cargando tareas: {e}")

    def actualizar_filtro_usuarios(self, usuarios):
        actuales = set(self.filtro_asignado.itemText(i) for i in range(self.filtro_asignado.count()))
        nuevos = sorted(u for u in usuarios if u and u not in actuales)

        if nuevos:
            self.filtro_asignado.blockSignals(True)
            for nuevo in nuevos:
                self.filtro_asignado.addItem(nuevo)
            self.filtro_asignado.blockSignals(False)

    def mover_tarea(self, tarea_id, nuevo_estado):
        try:
            actualizar_estado(tarea_id, nuevo_estado)
            self.recargar()
        except Exception as e:
            print(f"Error moviendo tarea: {e}")

    def crear_tarea(self):
        dialogo = DialogoTarea(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            if datos['titulo']:
                try:
                    crear_tarea(datos)
                    self.recargar()
                except Exception as e:
                    print(f"Error creando tarea: {e}")

    def gestionar_sprint(self):
        dialogo = DialogoSprint(self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            try:
                Sprint.crear(**datos)
                QMessageBox.information(self, "Sprint creado", "Sprint creado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear el sprint:\n{e}")

    def mostrar_reportes(self):
        dialogo = DialogoReportes(self)
        dialogo.exec_()

    def mostrar_reporte_tarea(self, tarea_id):
        tarea = Tarea.obtener_por_id(tarea_id)
        if not tarea:
            QMessageBox.warning(self, "Tarea no encontrada", f"No se encontró la tarea #{tarea_id}.")
            return

        texto = f"""\
📋 Reporte de Tarea #{tarea.id}

📌 Título: {tarea.titulo}
📖 Descripción: {tarea.descripcion}
⚙️ Tipo: {tarea.tipo}
🔥 Prioridad: {tarea.prioridad}
🧑‍💻 Asignado a: {tarea.asignado_a}
📆 Límite: {tarea.fecha_limite}
🏁 Estado: {tarea.estado}
🧩 Story Points: {tarea.story_points}
🗂️ Tags: {', '.join(tarea.tags)}
✅ Criterios: {tarea.criterios_aceptacion}
"""

        QMessageBox.information(self, f"Reporte Tarea #{tarea_id}", texto)

    def aplicar_filtros(self):
        self.recargar()

    def editar_tarea(self, tarea_id):
        tarea = Tarea.obtener_por_id(tarea_id)
        if not tarea:
            print(f"No se encontró la tarea con ID {tarea_id}")
            return

        dialogo = DialogoTarea(tarea=tarea, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            try:
                tarea.actualizar(
                    titulo=datos['titulo'],
                    descripcion=datos['descripcion'],
                    tipo=datos['tipo'],
                    prioridad=datos['prioridad'],
                    story_points=datos['story_points'],
                    asignado_a=datos['asignado'],
                    fecha_limite=datos['fecha_limite'],
                    criterios_aceptacion=datos['criterios'],
                    tags=','.join(datos['tags'])
                )
                self.recargar()
            except Exception as e:
                print(f"Error actualizando tarea: {e}")

    def eliminar_tarea(self, tarea_id):
        confirm = QMessageBox.question(
            self,
            "Eliminar Tarea",
            "¿Querés eliminar esta tarea? Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                tarea = Tarea.obtener_por_id(tarea_id)
                if tarea:
                    tarea.eliminar()
                    self.recargar()
            except Exception as e:
                print(f"Error eliminando tarea: {e}")
