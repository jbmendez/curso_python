"""
Implementación concreta del repositorio de ControlReferente usando SQLite
"""
import sqlite3
from typing import List, Optional
from datetime import datetime
from src.domain.entities.control_referente import ControlReferente
from src.domain.repositories.control_referente_repository import ControlReferenteRepository


class SQLiteControlReferenteRepository(ControlReferenteRepository):
    """Implementación del repositorio de asociaciones Control-Referente usando SQLite"""
    
    def __init__(self, db_path: str = "sistema_controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de asociaciones Control-Referente si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS control_referente (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    control_id INTEGER NOT NULL,
                    referente_id INTEGER NOT NULL,
                    activa BOOLEAN DEFAULT 1,
                    fecha_asociacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notificar_por_email BOOLEAN DEFAULT 1,
                    notificar_por_archivo BOOLEAN DEFAULT 0,
                    observaciones TEXT,
                    FOREIGN KEY (control_id) REFERENCES controles(id) ON DELETE CASCADE,
                    FOREIGN KEY (referente_id) REFERENCES referentes(id) ON DELETE CASCADE,
                    UNIQUE(control_id, referente_id)
                )
            """)
    
    def obtener_por_id(self, id: int) -> Optional[ControlReferente]:
        """Obtiene una asociación por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM control_referente WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_control_referente(row)
            return None
    
    def obtener_todos(self) -> List[ControlReferente]:
        """Obtiene todas las asociaciones"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM control_referente ORDER BY fecha_asociacion DESC")
            rows = cursor.fetchall()
            
            return [self._row_to_control_referente(row) for row in rows]
    
    def obtener_por_control(self, control_id: int) -> List[ControlReferente]:
        """Obtiene todas las asociaciones de un control específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM control_referente WHERE control_id = ? ORDER BY fecha_asociacion DESC",
                (control_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_control_referente(row) for row in rows]
    
    def obtener_por_referente(self, referente_id: int) -> List[ControlReferente]:
        """Obtiene todas las asociaciones de un referente específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM control_referente WHERE referente_id = ? ORDER BY fecha_asociacion DESC",
                (referente_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_control_referente(row) for row in rows]
    
    def obtener_activas(self) -> List[ControlReferente]:
        """Obtiene solo las asociaciones activas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM control_referente WHERE activa = 1 ORDER BY fecha_asociacion DESC"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_control_referente(row) for row in rows]
    
    def existe_asociacion(self, control_id: int, referente_id: int) -> bool:
        """Verifica si existe una asociación entre un control y referente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM control_referente WHERE control_id = ? AND referente_id = ?",
                (control_id, referente_id)
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    def guardar(self, control_referente: ControlReferente) -> ControlReferente:
        """Guarda una asociación (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if control_referente.id is None:
                # Crear nueva asociación
                cursor = conn.execute(
                    """INSERT INTO control_referente 
                       (control_id, referente_id, activa, fecha_asociacion, 
                        notificar_por_email, notificar_por_archivo, observaciones) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (control_referente.control_id, control_referente.referente_id, 
                     control_referente.activa,
                     control_referente.fecha_asociacion or datetime.now(),
                     control_referente.notificar_por_email,
                     control_referente.notificar_por_archivo,
                     control_referente.observaciones)
                )
                control_referente.id = cursor.lastrowid
            else:
                # Actualizar asociación existente
                conn.execute(
                    """UPDATE control_referente 
                       SET control_id=?, referente_id=?, activa=?, 
                           notificar_por_email=?, notificar_por_archivo=?, observaciones=? 
                       WHERE id=?""",
                    (control_referente.control_id, control_referente.referente_id,
                     control_referente.activa, control_referente.notificar_por_email,
                     control_referente.notificar_por_archivo, control_referente.observaciones,
                     control_referente.id)
                )
            
            return control_referente
    
    def eliminar(self, id: int) -> bool:
        """Elimina una asociación por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM control_referente WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def eliminar_por_control_referente(self, control_id: int, referente_id: int) -> bool:
        """Elimina una asociación específica entre control y referente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM control_referente WHERE control_id = ? AND referente_id = ?",
                (control_id, referente_id)
            )
            return cursor.rowcount > 0
    
    def _row_to_control_referente(self, row: sqlite3.Row) -> ControlReferente:
        """Convierte una fila de base de datos a una entidad ControlReferente"""
        fecha_asociacion = None
        if row['fecha_asociacion']:
            try:
                fecha_asociacion = datetime.fromisoformat(row['fecha_asociacion'])
            except:
                fecha_asociacion = datetime.now()
        
        return ControlReferente(
            id=row['id'],
            control_id=row['control_id'],
            referente_id=row['referente_id'],
            activa=bool(row['activa']),
            fecha_asociacion=fecha_asociacion,
            notificar_por_email=bool(row['notificar_por_email']),
            notificar_por_archivo=bool(row['notificar_por_archivo']),
            observaciones=row['observaciones'] or ""
        )