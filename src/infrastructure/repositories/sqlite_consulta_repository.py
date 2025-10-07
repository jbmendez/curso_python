"""
Implementación concreta del repositorio de Consulta usando SQLite
"""
import sqlite3
from typing import List, Optional
from src.domain.entities.consulta import Consulta
from src.domain.repositories.consulta_repository import ConsultaRepository


class SQLiteConsultaRepository(ConsultaRepository):
    """Implementación del repositorio de consultas usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de consultas si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    sql TEXT NOT NULL,
                    descripcion TEXT,
                    control_id INTEGER,
                    conexion_id INTEGER,
                    activa BOOLEAN DEFAULT 1,
                    FOREIGN KEY (control_id) REFERENCES controles(id),
                    FOREIGN KEY (conexion_id) REFERENCES conexiones(id)
                )
            """)
            
            # Verificar si las columnas nuevas existen y agregarlas si no
            cursor = conn.execute("PRAGMA table_info(consultas)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            if 'control_id' not in columnas:
                conn.execute("ALTER TABLE consultas ADD COLUMN control_id INTEGER")
            if 'conexion_id' not in columnas:
                conn.execute("ALTER TABLE consultas ADD COLUMN conexion_id INTEGER")
    
    def obtener_por_id(self, id: int) -> Optional[Consulta]:
        """Obtiene una consulta por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_consulta(row)
            return None
    
    def obtener_todos(self) -> List[Consulta]:
        """Obtiene todas las consultas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM consultas ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_consulta(row) for row in rows]
    
    def obtener_activas(self) -> List[Consulta]:
        """Obtiene solo las consultas activas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas WHERE activa = 1 ORDER BY nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_consulta(row) for row in rows]
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Consulta]:
        """Obtiene una consulta por su nombre"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas WHERE nombre = ?", (nombre,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_consulta(row)
            return None
    
    def obtener_por_ids(self, ids: List[int]) -> List[Consulta]:
        """Obtiene múltiples consultas por sus IDs"""
        if not ids:
            return []
        
        placeholders = ','.join('?' * len(ids))
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM consultas WHERE id IN ({placeholders})",
                ids
            )
            rows = cursor.fetchall()
            
            return [self._row_to_consulta(row) for row in rows]
    
    def obtener_por_control(self, control_id: int) -> List[Consulta]:
        """Obtiene todas las consultas de un control específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas WHERE control_id = ? ORDER BY nombre",
                (control_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_consulta(row) for row in rows]
    
    def guardar(self, consulta: Consulta) -> Consulta:
        """Guarda una consulta (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if consulta.id is None:
                # Crear nueva consulta
                cursor = conn.execute(
                    """INSERT INTO consultas (nombre, sql, descripcion, control_id, conexion_id, activa) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (consulta.nombre, consulta.sql, consulta.descripcion, 
                     consulta.control_id, consulta.conexion_id, consulta.activa)
                )
                consulta.id = cursor.lastrowid
            else:
                # Actualizar consulta existente
                conn.execute(
                    """UPDATE consultas 
                       SET nombre=?, sql=?, descripcion=?, control_id=?, conexion_id=?, activa=? 
                       WHERE id=?""",
                    (consulta.nombre, consulta.sql, consulta.descripcion,
                     consulta.control_id, consulta.conexion_id, consulta.activa, consulta.id)
                )
            
            return consulta
    
    def actualizar(self, consulta: Consulta) -> Consulta:
        """Actualiza una consulta existente"""
        return self.guardar(consulta)
    
    def eliminar(self, id: int) -> bool:
        """Elimina una consulta por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM consultas WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def _row_to_consulta(self, row: sqlite3.Row) -> Consulta:
        """Convierte una fila de base de datos a una entidad Consulta"""
        return Consulta(
            id=row['id'],
            nombre=row['nombre'],
            sql=row['sql'],
            descripcion=row['descripcion'] if row['descripcion'] else "",
            control_id=row['control_id'] if 'control_id' in row.keys() else None,
            conexion_id=row['conexion_id'] if 'conexion_id' in row.keys() else None,
            activa=bool(row['activa'])
        )