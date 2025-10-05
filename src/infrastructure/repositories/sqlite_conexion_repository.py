"""
Implementación concreta del repositorio de Conexión usando SQLite
"""
import sqlite3
from typing import List, Optional
from src.domain.entities.conexion import Conexion
from src.domain.repositories.conexion_repository import ConexionRepository


class SQLiteConexionRepository(ConexionRepository):
    """Implementación del repositorio de conexiones usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de conexiones si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conexiones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    base_datos TEXT NOT NULL,
                    servidor TEXT NOT NULL,
                    puerto INTEGER,
                    usuario TEXT NOT NULL,
                    contraseña TEXT NOT NULL,
                    tipo_motor TEXT DEFAULT 'postgresql',
                    activa BOOLEAN DEFAULT 1
                )
            """)
    
    def obtener_por_id(self, id: int) -> Optional[Conexion]:
        """Obtiene una conexión por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM conexiones WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_conexion(row)
            return None
    
    def obtener_todos(self) -> List[Conexion]:
        """Obtiene todas las conexiones"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM conexiones ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_conexion(row) for row in rows]
    
    def obtener_activas(self) -> List[Conexion]:
        """Obtiene solo las conexiones activas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM conexiones WHERE activa = 1 ORDER BY nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_conexion(row) for row in rows]
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Conexion]:
        """Obtiene una conexión por su nombre"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM conexiones WHERE nombre = ?", (nombre,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_conexion(row)
            return None
    
    def guardar(self, conexion: Conexion) -> Conexion:
        """Guarda una conexión (crear o actualizar)"""
        with sqlite3.connect(self.db_path) as conn:
            if conexion.id is None:
                # Crear nueva conexión
                cursor = conn.execute(
                    """INSERT INTO conexiones 
                       (nombre, base_datos, servidor, puerto, usuario, contraseña, tipo_motor, activa) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (conexion.nombre, conexion.base_datos, conexion.servidor, conexion.puerto,
                     conexion.usuario, conexion.contraseña, conexion.tipo_motor, conexion.activa)
                )
                conexion.id = cursor.lastrowid
            else:
                # Actualizar conexión existente
                conn.execute(
                    """UPDATE conexiones 
                       SET nombre=?, base_datos=?, servidor=?, puerto=?, usuario=?, 
                           contraseña=?, tipo_motor=?, activa=? 
                       WHERE id=?""",
                    (conexion.nombre, conexion.base_datos, conexion.servidor, conexion.puerto,
                     conexion.usuario, conexion.contraseña, conexion.tipo_motor, 
                     conexion.activa, conexion.id)
                )
            
            return conexion
    
    def eliminar(self, id: int) -> bool:
        """Elimina una conexión por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM conexiones WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def probar_conexion(self, conexion: Conexion) -> bool:
        """Prueba si la conexión funciona correctamente"""
        # TODO: Implementar prueba real de conexión
        # Por ahora, solo validamos que la configuración sea válida
        return conexion.es_configuracion_valida()
    
    def _row_to_conexion(self, row: sqlite3.Row) -> Conexion:
        """Convierte una fila de base de datos a una entidad Conexión"""
        return Conexion(
            id=row['id'],
            nombre=row['nombre'],
            base_datos=row['base_datos'],
            servidor=row['servidor'],
            puerto=row['puerto'],
            usuario=row['usuario'],
            contraseña=row['contraseña'],
            tipo_motor=row['tipo_motor'],
            activa=bool(row['activa'])
        )