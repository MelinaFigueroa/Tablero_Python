from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QApplication
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QColor


class Tarjeta(QFrame):
    """Tarjeta de tarea con info visual y drag & drop"""

    editada = pyqtSignal(int)
    eliminada = pyqtSignal(int)
    reportada = pyqtSignal(int)
    
    def __init__(self, tarea_id, titulo, descripcion, tipo="Task", prioridad="Media",
                 asignado="", story_points=0, tags=None):
        super().__init__()
        self.tarea_id = tarea_id
        self.tipo = tipo
        self.prioridad = prioridad
        self.tags = tags or []

        self.setObjectName("tarjeta")
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")

        self.setupUI(titulo, descripcion, asignado, story_points)

    def setupUI(self, titulo, descripcion, asignado, story_points):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Header: Tipo y Prioridad
        header = QHBoxLayout()
        tipo_label = QLabel(self.tipo)
        tipo_label.setObjectName("tipo-label")
        prioridad_label = QLabel(self.prioridad)
        prioridad_label.setObjectName("prioridad-label")
        header.addWidget(tipo_label)
        header.addStretch()
        header.addWidget(prioridad_label)
        layout.addLayout(header)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setWordWrap(True)
        titulo_label.setObjectName("titulo-tarjeta")
        layout.addWidget(titulo_label)

        # Descripción truncada
        if descripcion:
            desc = descripcion[:80] + "..." if len(descripcion) > 80 else descripcion
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setObjectName("descripcion-tarjeta")
            layout.addWidget(desc_label)

        # Footer: asignado y story points
        footer = QHBoxLayout()
        if asignado:
            iniciales = "".join([parte[0] for parte in asignado.strip().split()[:2]]).upper()
            circulo = QLabel(iniciales)
            circulo.setFixedSize(24, 24)
            circulo.setAlignment(Qt.AlignCenter)
            circulo.setStyleSheet("""
                background-color: #0077B6;
                color: white;
                font-weight: bold;
                border-radius: 12px;
            """)

            footer.addWidget(circulo)
            footer.addWidget(QLabel(asignado))


        if story_points > 0:
            btn_reportar = QToolButton()
            btn_reportar.setText("📊")
            btn_reportar.setToolTip("Ver reporte de tarea")
            btn_reportar.setStyleSheet("QToolButton { font-size: 14px; padding: 0px; }")
            btn_reportar.clicked.connect(lambda: self.reportada.emit(self.tarea_id))
            footer.addWidget(btn_reportar)

        footer.addStretch()

        # Botón editar
        btn_editar = QToolButton()
        btn_editar.setText("⚙️")
        btn_editar.setToolTip("Editar tarea")
        btn_editar.clicked.connect(lambda: self.editada.emit(self.tarea_id))
        footer.addWidget(btn_editar)

        # Botón eliminar
        btn_eliminar = QToolButton()
        btn_eliminar.setText("🗑️")
        btn_eliminar.setToolTip("Eliminar tarea")
        btn_eliminar.clicked.connect(lambda: self.eliminada.emit(self.tarea_id))
        footer.addWidget(btn_eliminar)

        layout.addLayout(footer)

        # Tags
        if self.tags:
            tags_label = QLabel(" ".join([f"#{tag}" for tag in self.tags[:3]]))
            tags_label.setObjectName("tags")
            layout.addWidget(tags_label)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(str(self.tarea_id))
        drag.setMimeData(mimedata)

        # Crear pixmap como preview visual
        pixmap = QPixmap(self.size())
        self.render(pixmap)

        # Hacerlo semitransparente
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 180))
        painter.end()

        drag.setPixmap(pixmap)
        drag.exec_(Qt.MoveAction)
