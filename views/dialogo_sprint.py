from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit, QDateEdit,
    QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import QDate
from models.sprint import Sprint

class DialogoSprint(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏃 Nuevo Sprint")
        self.setFixedSize(400, 300)

        layout = QFormLayout(self)

        self.nombre_edit = QLineEdit()
        self.objetivo_edit = QTextEdit()

        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_inicio.setCalendarPopup(True)

        self.fecha_fin = QDateEdit()
        self.fecha_fin.setDate(QDate.currentDate().addDays(14))
        self.fecha_fin.setCalendarPopup(True)

        layout.addRow("📛 Nombre:", self.nombre_edit)
        layout.addRow("🎯 Objetivo:", self.objetivo_edit)
        layout.addRow("📅 Inicio:", self.fecha_inicio)
        layout.addRow("📅 Fin:", self.fecha_fin)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.validar_y_aceptar)
        botones.rejected.connect(self.reject)

        layout.addRow(botones)

    def validar_y_aceptar(self):
        if not self.nombre_edit.text().strip():
            QMessageBox.warning(self, "Falta nombre", "El nombre del sprint no puede estar vacío.")
            return
        if self.fecha_fin.date() < self.fecha_inicio.date():
            QMessageBox.warning(self, "Fechas incorrectas", "La fecha de fin no puede ser anterior a la de inicio.")
            return
        self.accept()

    def obtener_datos(self):
        return {
            "nombre": self.nombre_edit.text().strip(),
            "objetivo": self.objetivo_edit.toPlainText().strip(),
            "fecha_inicio": self.fecha_inicio.date().toPyDate(),
            "fecha_fin": self.fecha_fin.date().toPyDate()
        }
