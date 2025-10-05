"""
Implementación concreta del repositorio de Usuario usando SQLite

Esta es la implementación real que maneja la persistencia de datos.
Implementa la interface definida en el dominio.
"""
import sqlite3
from typing import List, Optional
from datetime import datetime
from src.domain.entities.usuario import Usuario
from src.domain.repositories.usuario_repository import UsuarioRepository


class SQLiteUsuarioRepository(UsuarioRepository):
    """Implementación del repositorio usando SQLite"""
    
    def __init__(self, db_path: str = "usuarios.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de usuarios si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    fecha_creacion TIMESTAMP,
                    activo BOOLEAN
                )
            """)
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM usuarios WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return Usuario(
                    id=row['id'],
                    nombre=row['nombre'],
                    email=row['email'],
                    fecha_creacion=datetime.fromisoformat(row['fecha_creacion']),
                    activo=bool(row['activo'])
                )
            return None
    
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            
            return [
                Usuario(
                    id=row['id'],
                    nombre=row['nombre'],
                    email=row['email'],
                    fecha_creacion=datetime.fromisoformat(row['fecha_creacion']),
                    activo=bool(row['activo'])
                )
                for row in rows
            ]
    
    def guardar(self, usuario: Usuario) -> Usuario:
        """Guarda un usuario (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if usuario.id is None:
                # Crear nuevo usuario
                cursor = conn.execute(
                    """INSERT INTO usuarios (nombre, email, fecha_creacion, activo) 
                       VALUES (?, ?, ?, ?)""",
                    (usuario.nombre, usuario.email, 
                     usuario.fecha_creacion.isoformat(), usuario.activo)
                )
                usuario.id = cursor.lastrowid
            else:
                # Actualizar usuario existente
                conn.execute(
                    """UPDATE usuarios 
                       SET nombre=?, email=?, activo=? 
                       WHERE id=?""",
                    (usuario.nombre, usuario.email, usuario.activo, usuario.id)
                )
            
            return usuario
    
    def eliminar(self, id: int) -> bool:
        """Elimina un usuario por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM usuarios WHERE email = ?", (email,)
            )
            row = cursor.fetchone()
            
            if row:
                return Usuario(
                    id=row['id'],
                    nombre=row['nombre'],
                    email=row['email'],
                    fecha_creacion=datetime.fromisoformat(row['fecha_creacion']),
                    activo=bool(row['activo'])
                )
            return None