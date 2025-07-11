from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from models.sprint import Sprint

class VistaSprints(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📋 Sprints del Proyecto")
        self.setMinimumSize(600, 400)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)  # Se cierra al hacer clic fuera
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("border: 1px solid #ccc; background-color: white;")

        layout = QVBoxLayout(self)

        self.lista_sprints = QListWidget()
        layout.addWidget(QLabel("🗂 Lista de Sprints:"))
        layout.addWidget(self.lista_sprints)

        self.cargar_sprints()
        self.centrar_en_pantalla()

    def cargar_sprints(self):
        self.lista_sprints.clear()
        conn = Sprint.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints ORDER BY fecha_inicio DESC")
        sprints = cursor.fetchall()
        conn.close()

        for sprint in sprints:
            sprint_obj = Sprint(*sprint)
            item_text = f"📛 {sprint_obj.nombre} | {sprint_obj.estado} | {sprint_obj.fecha_inicio} ➡ {sprint_obj.fecha_fin}\n🎯 {sprint_obj.objetivo}"
            item = QListWidgetItem(item_text)
            self.lista_sprints.addItem(item)

    def centrar_en_pantalla(self):
        pantalla = self.screen().availableGeometry()
        self.adjustSize()
        tamaño = self.geometry()
        x = (pantalla.width() - tamaño.width()) // 2
        y = (pantalla.height() - tamaño.height()) // 2
        self.move(x, y)
