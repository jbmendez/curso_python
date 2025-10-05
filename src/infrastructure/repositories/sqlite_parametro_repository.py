"""
Implementación concreta del repositorio de Parámetro usando SQLite
"""
import sqlite3
from typing import List, Optional
from src.domain.entities.parametro import Parametro, TipoParametro
from src.domain.repositories.parametro_repository import ParametroRepository


class SQLiteParametroRepository(ParametroRepository):
    """Implementación del repositorio de parámetros usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de parámetros si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS parametros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    tipo TEXT NOT NULL,
                    descripcion TEXT,
                    valor_por_defecto TEXT,
                    obligatorio BOOLEAN DEFAULT 1
                )
            """)
    
    def obtener_por_id(self, id: int) -> Optional[Parametro]:
        """Obtiene un parámetro por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM parametros WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_parametro(row)
            return None
    
    def obtener_todos(self) -> List[Parametro]:
        """Obtiene todos los parámetros"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM parametros ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_parametro(row) for row in rows]
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Parametro]:
        """Obtiene un parámetro por su nombre"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM parametros WHERE nombre = ?", (nombre,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_parametro(row)
            return None
    
    def obtener_por_ids(self, ids: List[int]) -> List[Parametro]:
        """Obtiene múltiples parámetros por sus IDs"""
        if not ids:
            return []
        
        placeholders = ','.join('?' * len(ids))
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM parametros WHERE id IN ({placeholders})",
                ids
            )
            rows = cursor.fetchall()
            
            return [self._row_to_parametro(row) for row in rows]
    
    def guardar(self, parametro: Parametro) -> Parametro:
        """Guarda un parámetro (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if parametro.id is None:
                # Crear nuevo parámetro
                cursor = conn.execute(
                    """INSERT INTO parametros (nombre, tipo, descripcion, valor_por_defecto, obligatorio) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (parametro.nombre, parametro.tipo.value, parametro.descripcion,
                     parametro.valor_por_defecto, parametro.obligatorio)
                )
                parametro.id = cursor.lastrowid
            else:
                # Actualizar parámetro existente
                conn.execute(
                    """UPDATE parametros 
                       SET nombre=?, tipo=?, descripcion=?, valor_por_defecto=?, obligatorio=? 
                       WHERE id=?""",
                    (parametro.nombre, parametro.tipo.value, parametro.descripcion,
                     parametro.valor_por_defecto, parametro.obligatorio, parametro.id)
                )
            
            return parametro
    
    def eliminar(self, id: int) -> bool:
        """Elimina un parámetro por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM parametros WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def _row_to_parametro(self, row: sqlite3.Row) -> Parametro:
        """Convierte una fila de base de datos a una entidad Parámetro"""
        return Parametro(
            id=row['id'],
            nombre=row['nombre'],
            tipo=TipoParametro(row['tipo']),
            descripcion=row['descripcion'],
            valor_por_defecto=row['valor_por_defecto'],
            obligatorio=bool(row['obligatorio'])
        )