from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import sqlite3
import hashlib


@dataclass
class Usuario:
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    password: str = ""
    rol: str = "Developer"  # ScrumMaster, ProductOwner, Tester, etc.
    fecha_registro: datetime = None

    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def crear(cls, nombre, email, password, rol="Developer"):
        usuario = cls(
            nombre=nombre.strip(),
            email=email.strip().lower(),
            password=cls.hash_password(password),
            rol=rol
        )
        conn = sqlite3.connect("agileflow.db")
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password, rol, fecha_registro)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                usuario.nombre,
                usuario.email,
                usuario.password,
                usuario.rol,
                usuario.fecha_registro.isoformat()
            ))
            usuario.id = cursor.lastrowid
            conn.commit()
            return usuario
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error creando usuario: {e}")
        finally:
            conn.close()

    @classmethod
    def login(cls, email: str, password: str) -> Optional['Usuario']:
        conn = sqlite3.connect("agileflow.db")
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            row = cursor.fetchone()
            if row and row[3] == cls.hash_password(password):
                return cls(
                    id=row[0],
                    nombre=row[1],
                    email=row[2],
                    password=row[3],
                    rol=row[4],
                    fecha_registro=datetime.fromisoformat(row[5])
                )
            return None
        except sqlite3.Error as e:
            raise Exception(f"Error en login: {e}")
        finally:
            conn.close()
