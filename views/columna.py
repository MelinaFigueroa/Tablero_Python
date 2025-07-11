# views/columna.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal


class ColumnaKanban(QWidget):
    """Columna optimizada con drag & drop mejorado"""

    tarea_movida = pyqtSignal(int, str)  # Signal para notificar cambios al tablero

    def __init__(self, estado, titulo=None):
        super().__init__()
        self.estado = estado
        self.titulo = titulo or estado.value
        self.tareas = []
        self.setupUI()

    def setupUI(self):
        self.setAcceptDrops(True)
        self.setMinimumWidth(280)
        self.setMaximumWidth(320)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header de la columna
        header = QFrame()
        header.setObjectName(f"header-{self.estado.name.lower()}")
        header_layout = QVBoxLayout(header)

        self.titulo_label = QLabel(self.titulo)
        self.titulo_label.setObjectName("titulo-columna")
        self.titulo_label.setAlignment(Qt.AlignCenter)

        self.contador_label = QLabel("0 tareas")
        self.contador_label.setObjectName("contador-columna")
        self.contador_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(self.titulo_label)
        header_layout.addWidget(self.contador_label)
        layout.addWidget(header)

        # Área de scroll para tarjetas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(8)
        self.content_layout.addStretch()  # Empuja tarjetas hacia arriba

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

        # Nombre para aplicar estilos CSS
        self.setObjectName(f"columna-{self.estado.name.lower()}")

    def agregar_tarjeta(self, tarjeta):
        """Agrega una tarjeta visual a la columna"""
        self.tareas.append(tarjeta)
        self.content_layout.insertWidget(self.content_layout.count() - 1, tarjeta)
        self.actualizar_contador()

    def remover_tarjeta(self, tarjeta):
        """Quita una tarjeta visual de la columna"""
        if tarjeta in self.tareas:
            self.tareas.remove(tarjeta)
            self.content_layout.removeWidget(tarjeta)
            tarjeta.setParent(None)
            self.actualizar_contador()

    def limpiar(self):
        """Elimina todas las tarjetas de la columna"""
        for tarjeta in self.tareas[:]:
            self.remover_tarjeta(tarjeta)

    def actualizar_contador(self):
        """Actualiza el número de tareas mostradas"""
        count = len(self.tareas)
        self.contador_label.setText(f"{count} tarea{'s' if count != 1 else ''}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        try:
            tarea_id = int(event.mimeData().text())
            self.tarea_movida.emit(tarea_id, self.estado.value)
            event.acceptProposedAction()
        except ValueError:
            event.ignore()
