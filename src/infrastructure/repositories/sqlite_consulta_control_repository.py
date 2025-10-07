"""
Implementación SQLite del repositorio ConsultaControl
"""
import sqlite3
from typing import List, Optional
from datetime import datetime
from src.domain.entities.consulta_control import ConsultaControl
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository


class SQLiteConsultaControlRepository(ConsultaControlRepository):
    """Implementación SQLite del repositorio ConsultaControl"""
    
    def __init__(self, db_path: str = "sistema_controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de asociaciones consulta-control si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS consultas_controles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    control_id INTEGER NOT NULL,
                    consulta_id INTEGER NOT NULL,
                    es_disparo BOOLEAN DEFAULT 0,
                    orden INTEGER DEFAULT 1,
                    activa BOOLEAN DEFAULT 1,
                    fecha_asociacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (control_id) REFERENCES controles(id) ON DELETE CASCADE,
                    FOREIGN KEY (consulta_id) REFERENCES consultas(id) ON DELETE CASCADE,
                    UNIQUE(control_id, consulta_id)
                )
            """)
            
            # Crear índices para mejorar el rendimiento
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_consultas_controles_control 
                ON consultas_controles(control_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_consultas_controles_consulta 
                ON consultas_controles(consulta_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_consultas_controles_disparo 
                ON consultas_controles(control_id, es_disparo)
            """)
    
    def obtener_por_id(self, id: int) -> Optional[ConsultaControl]:
        """Obtiene una asociación por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas_controles WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_consulta_control(row)
            return None
    
    def obtener_por_control(self, control_id: int) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones de un control específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas_controles WHERE control_id = ? AND activa = 1 ORDER BY orden, id",
                (control_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_consulta_control(row) for row in rows]
    
    def obtener_por_consulta(self, consulta_id: int) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones de una consulta específica"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas_controles WHERE consulta_id = ? AND activa = 1",
                (consulta_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_consulta_control(row) for row in rows]
    
    def obtener_disparo_por_control(self, control_id: int) -> Optional[ConsultaControl]:
        """Obtiene la consulta de disparo de un control específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM consultas_controles WHERE control_id = ? AND es_disparo = 1 AND activa = 1",
                (control_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_consulta_control(row)
            return None
    
    def guardar(self, asociacion: ConsultaControl) -> ConsultaControl:
        """Guarda una asociación (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if asociacion.id is None:
                # Crear nueva asociación
                cursor = conn.execute(
                    """INSERT INTO consultas_controles 
                       (control_id, consulta_id, es_disparo, orden, activa, fecha_asociacion) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (asociacion.control_id, asociacion.consulta_id, asociacion.es_disparo,
                     asociacion.orden, asociacion.activa, asociacion.fecha_asociacion)
                )
                asociacion.id = cursor.lastrowid
            else:
                # Actualizar asociación existente
                conn.execute(
                    """UPDATE consultas_controles 
                       SET control_id=?, consulta_id=?, es_disparo=?, orden=?, activa=? 
                       WHERE id=?""",
                    (asociacion.control_id, asociacion.consulta_id, asociacion.es_disparo,
                     asociacion.orden, asociacion.activa, asociacion.id)
                )
            
            return asociacion
    
    def eliminar(self, id: int) -> bool:
        """Elimina una asociación por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM consultas_controles WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def eliminar_por_control(self, control_id: int) -> bool:
        """Elimina todas las asociaciones de un control"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM consultas_controles WHERE control_id = ?", (control_id,))
            return cursor.rowcount > 0
    
    def eliminar_por_consulta(self, consulta_id: int) -> bool:
        """Elimina todas las asociaciones de una consulta"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM consultas_controles WHERE consulta_id = ?", (consulta_id,))
            return cursor.rowcount > 0
    
    def establecer_consulta_disparo(self, control_id: int, consulta_id: int) -> bool:
        """Establece una consulta como la de disparo para un control"""
        with sqlite3.connect(self.db_path) as conn:
            # Primero quitar el flag de disparo de todas las consultas del control
            conn.execute(
                "UPDATE consultas_controles SET es_disparo = 0 WHERE control_id = ?",
                (control_id,)
            )
            
            # Luego establecer la nueva consulta como disparo
            cursor = conn.execute(
                "UPDATE consultas_controles SET es_disparo = 1 WHERE control_id = ? AND consulta_id = ?",
                (control_id, consulta_id)
            )
            
            return cursor.rowcount > 0
    
    def obtener_todas(self) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM consultas_controles ORDER BY control_id, orden")
            rows = cursor.fetchall()
            
            return [self._row_to_consulta_control(row) for row in rows]
    
    def _row_to_consulta_control(self, row) -> ConsultaControl:
        """Convierte una fila de la base de datos a una entidad ConsultaControl"""
        fecha_asociacion = None
        if row['fecha_asociacion']:
            try:
                fecha_asociacion = datetime.fromisoformat(row['fecha_asociacion'])
            except:
                fecha_asociacion = datetime.now()
        
        return ConsultaControl(
            id=row['id'],
            control_id=row['control_id'],
            consulta_id=row['consulta_id'],
            es_disparo=bool(row['es_disparo']),
            orden=row['orden'],
            activa=bool(row['activa']),
            fecha_asociacion=fecha_asociacion
        )