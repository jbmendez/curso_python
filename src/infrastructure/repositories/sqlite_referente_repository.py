"""
Implementación concreta del repositorio de Referente usando SQLite
"""
import sqlite3
from typing import List, Optional
from src.domain.entities.referente import Referente
from src.domain.repositories.referente_repository import ReferenteRepository


class SQLiteReferenteRepository(ReferenteRepository):
    """Implementación del repositorio de referentes usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de referentes si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS referentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    path_archivos TEXT,
                    activo BOOLEAN DEFAULT 1
                )
            """)
            
            # Migrar datos si es necesario
            cursor = conn.execute("PRAGMA table_info(referentes)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            # Si existe carpeta_red pero no path_archivos, migrar
            if 'carpeta_red' in columnas and 'path_archivos' not in columnas:
                try:
                    conn.execute("ALTER TABLE referentes ADD COLUMN path_archivos TEXT")
                    conn.execute("UPDATE referentes SET path_archivos = carpeta_red")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        raise
            # Si no existe path_archivos (tabla nueva), agregarla
            elif 'path_archivos' not in columnas:
                try:
                    conn.execute("ALTER TABLE referentes ADD COLUMN path_archivos TEXT")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        raise
    
    def obtener_por_id(self, id: int) -> Optional[Referente]:
        """Obtiene un referente por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM referentes WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_referente(row)
            return None
    
    def obtener_todos(self) -> List[Referente]:
        """Obtiene todos los referentes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM referentes ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_referente(row) for row in rows]
    
    def obtener_activos(self) -> List[Referente]:
        """Obtiene solo los referentes activos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM referentes WHERE activo = 1 ORDER BY nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_referente(row) for row in rows]
    
    def obtener_por_email(self, email: str) -> Optional[Referente]:
        """Obtiene un referente por su email"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM referentes WHERE email = ?", (email,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_referente(row)
            return None
    
    def obtener_por_ids(self, ids: List[int]) -> List[Referente]:
        """Obtiene múltiples referentes por sus IDs"""
        if not ids:
            return []
        
        placeholders = ','.join('?' * len(ids))
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM referentes WHERE id IN ({placeholders})",
                ids
            )
            rows = cursor.fetchall()
            
            return [self._row_to_referente(row) for row in rows]
    
    def guardar(self, referente: Referente) -> Referente:
        """Guarda un referente (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if referente.id is None:
                # Crear nuevo referente
                cursor = conn.execute(
                    """INSERT INTO referentes 
                       (nombre, email, path_archivos, activo) 
                       VALUES (?, ?, ?, ?)""",
                    (referente.nombre, referente.email, referente.path_archivos, referente.activo)
                )
                referente.id = cursor.lastrowid
            else:
                # Actualizar referente existente
                conn.execute(
                    """UPDATE referentes 
                       SET nombre=?, email=?, path_archivos=?, activo=? 
                       WHERE id=?""",
                    (referente.nombre, referente.email, referente.path_archivos, referente.activo, referente.id)
                )
            
            return referente
    
    def eliminar(self, id: int) -> bool:
        """Elimina un referente por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM referentes WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def _row_to_referente(self, row: sqlite3.Row) -> Referente:
        """Convierte una fila de base de datos a una entidad Referente"""
        return Referente(
            id=row['id'],
            nombre=row['nombre'],
            email=row['email'],
            path_archivos=row['path_archivos'] if 'path_archivos' in row.keys() else (row.get('carpeta_red') or ""),
            activo=bool(row['activo'])
        )