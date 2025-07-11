# 🧠 AgileFlow - Gestor de Tareas tipo Scrum

**Autora:** Melina Figueroa  
**Email:** melina.figueroa.89@gmail.com

---

## 📋 Descripción

**AgileFlow** es una aplicación de escritorio construida con **Python y PyQt5** que permite gestionar tareas dentro de un entorno ágil, siguiendo la metodología **Scrum/Kanban**.

Permite crear, mover y editar tareas, filtrarlas por prioridad o usuario, gestionar sprints y visualizar reportes como gráficos de burndown. Toda la información se almacena de forma persistente en una base de datos SQLite.

---

## 🧩 Características principales

✅ Interfaz gráfica intuitiva (PyQt5)  
✅ CRUD completo de tareas (crear, editar, mover, eliminar)  
✅ Gestión de sprints (crear, ver métricas)  
✅ Filtros por usuario y prioridad  
✅ Reportes visuales (Burndown chart)  
✅ Base de datos local (SQLite)  
✅ Estilos visuales personalizados con QSS

---

## 🔧 Requisitos

- Python 3.10 o superior  
- Sistema operativo Windows, Linux o macOS

### 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/MelinaFigueroa/Tablero_Python.git
```
  
  cd Tablero_Python


2. Instalar las dependencias:
pip install -r requirements.txt


## ▶️ Ejecución

3. Para iniciar la aplicación, ejecutar:
```bash
python main.py
```

**La base de datos agileflow.db se creará automáticamente si no existe.**

📁 Estructura del Proyecto
--
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── agileflow.db
    ├── /models
    │   ├── tarea.py
    │   ├── sprint.py
    │   └── usuario.py
    ├── /views
    │   ├── tablero.py
    │   ├── tarjeta.py
    │   ├── columna.py
    │   ├── dialogo_sprint.py
    │   ├── dialogo_reportes.py
    │   └── vista_sprints.py
    ├── /controllers
    │   └── tarea_controller.py
    ├── /database
    │   └── db.py
    └── /views/estilos.qss

## ⚠️ Notas adicionales

__Todos los datos se guardan localmente en agileflow.db__

_Se recomienda una **resolución mínima de 1366x768** para una mejor experiencia_

El proyecto no requiere conexión a internet

## 💌 Contacto
**Si tenés dudas, sugerencias o querés colaborar:**

📧 *melina.figueroa.89@gmail.com*
🐧 *@penguicoder9420 (Instagram)*

Disfrutá usar AgileFlow para organizar tu flujo de trabajo 🎯
