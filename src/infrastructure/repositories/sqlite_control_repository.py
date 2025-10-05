"""
Implementación concreta del repositorio de Control usando SQLite

Esta implementación maneja la persistencia de controles y sus relaciones
"""
import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from src.domain.entities.control import Control
from src.domain.repositories.control_repository import ControlRepository


class SQLiteControlRepository(ControlRepository):
    """Implementación del repositorio de controles usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tablas()
    
    def _crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabla principal de controles
            conn.execute("""
                CREATE TABLE IF NOT EXISTS controles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    descripcion TEXT,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP,
                    disparar_si_hay_datos BOOLEAN DEFAULT 1,
                    conexion_id INTEGER,
                    consulta_disparo_id INTEGER,
                    parametros_ids TEXT,  -- JSON array
                    consultas_a_disparar_ids TEXT,  -- JSON array
                    referentes_ids TEXT  -- JSON array
                )
            """)
    
    def obtener_por_id(self, id: int) -> Optional[Control]:
        """Obtiene un control por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM controles WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_control(row)
            return None
    
    def obtener_todos(self) -> List[Control]:
        """Obtiene todos los controles"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM controles ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_control(row) for row in rows]
    
    def obtener_activos(self) -> List[Control]:
        """Obtiene solo los controles activos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM controles WHERE activo = 1 ORDER BY nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_control(row) for row in rows]
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Control]:
        """Obtiene un control por su nombre"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM controles WHERE nombre = ?", (nombre,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_control(row)
            return None
    
    def guardar(self, control: Control) -> Control:
        """Guarda un control (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if control.id is None:
                # Crear nuevo control
                cursor = conn.execute(
                    """INSERT INTO controles 
                       (nombre, descripcion, activo, fecha_creacion, disparar_si_hay_datos,
                        conexion_id, consulta_disparo_id, parametros_ids, 
                        consultas_a_disparar_ids, referentes_ids) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        control.nombre,
                        control.descripcion,
                        control.activo,
                        control.fecha_creacion.isoformat() if control.fecha_creacion else None,
                        control.disparar_si_hay_datos,
                        control.conexion_id,
                        control.consulta_disparo_id,
                        json.dumps(control.parametros_ids),
                        json.dumps(control.consultas_a_disparar_ids),
                        json.dumps(control.referentes_ids)
                    )
                )
                control.id = cursor.lastrowid
            else:
                # Actualizar control existente
                conn.execute(
                    """UPDATE controles 
                       SET nombre=?, descripcion=?, activo=?, disparar_si_hay_datos=?,
                           conexion_id=?, consulta_disparo_id=?, parametros_ids=?,
                           consultas_a_disparar_ids=?, referentes_ids=?
                       WHERE id=?""",
                    (
                        control.nombre,
                        control.descripcion,
                        control.activo,
                        control.disparar_si_hay_datos,
                        control.conexion_id,
                        control.consulta_disparo_id,
                        json.dumps(control.parametros_ids),
                        json.dumps(control.consultas_a_disparar_ids),
                        json.dumps(control.referentes_ids),
                        control.id
                    )
                )
            
            return control
    
    def eliminar(self, id: int) -> bool:
        """Elimina un control por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM controles WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def cargar_relaciones(self, control: Control) -> Control:
        """Carga todas las relaciones de un control"""
        # En una implementación real, aquí cargaríamos las entidades relacionadas
        # desde sus respectivos repositorios. Por ahora, solo retornamos el control.
        # TODO: Implementar carga de relaciones cuando estén disponibles los otros repositorios
        return control
    
    def _row_to_control(self, row: sqlite3.Row) -> Control:
        """Convierte una fila de base de datos a una entidad Control"""
        return Control(
            id=row['id'],
            nombre=row['nombre'],
            descripcion=row['descripcion'],
            activo=bool(row['activo']),
            fecha_creacion=datetime.fromisoformat(row['fecha_creacion']) if row['fecha_creacion'] else None,
            disparar_si_hay_datos=bool(row['disparar_si_hay_datos']),
            conexion_id=row['conexion_id'],
            consulta_disparo_id=row['consulta_disparo_id'],
            parametros_ids=json.loads(row['parametros_ids']) if row['parametros_ids'] else [],
            consultas_a_disparar_ids=json.loads(row['consultas_a_disparar_ids']) if row['consultas_a_disparar_ids'] else [],
            referentes_ids=json.loads(row['referentes_ids']) if row['referentes_ids'] else []
        )