import sqlite3

def get_connection():
   return sqlite3.connect("agileflow.db", timeout=10, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL
        )
    ''')

    # Tabla de sprints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            objetivo TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            estado TEXT DEFAULT 'Planificado',
            velocidad_estimada INTEGER DEFAULT 0
        )
    ''')

    # Tabla de tareas (completa y actualizada)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            tipo TEXT DEFAULT 'Task',
            prioridad TEXT DEFAULT 'Media',
            estado TEXT DEFAULT 'To Do',
            story_points INTEGER DEFAULT 0,
            asignado_a TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            fecha_completado TEXT,
            criterios_aceptacion TEXT,
            tags TEXT,
            tiempo_estimado INTEGER DEFAULT 0,
            tiempo_real INTEGER DEFAULT 0,
            sprint_id INTEGER,
            epic_id INTEGER,
            FOREIGN KEY (sprint_id) REFERENCES sprints(id)
        )
    ''')

    conn.commit()
    conn.close()
