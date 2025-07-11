# main.py (optimizado)
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from views.tablero import TableroKanban
from database.db import init_db

def main():
    # Configuración de la aplicación
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("AgileFlow")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("AgileFlow Dev")
    
    # Inicializar base de datos
    try:
        init_db()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        sys.exit(1)
    
    # Crear y mostrar ventana principal
    ventana = TableroKanban()
    ventana.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()