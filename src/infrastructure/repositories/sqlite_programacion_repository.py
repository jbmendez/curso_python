"""
Implementación SQLite del repositorio de programaciones

Maneja la persistencia de programaciones de controles en base de datos SQLite
con soporte para diferentes tipos de programación y consultas especializadas.
"""
import sqlite3
import json
from datetime import datetime, time
from typing import List, Optional

from ...domain.repositories.programacion_repository import ProgramacionRepository
from ...domain.entities.programacion import Programacion, TipoProgramacion, DiaSemana


class SQLiteProgramacionRepository(ProgramacionRepository):
    """Implementación SQLite del repositorio de programaciones"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._crear_tabla_si_no_existe()
    
    def _crear_tabla_si_no_existe(self):
        """Crea la tabla programaciones si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS programaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    control_id INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    tipo_programacion TEXT NOT NULL,
                    activo BOOLEAN NOT NULL DEFAULT 1,
                    
                    -- Configuración de horario
                    hora_ejecucion TEXT,
                    fecha_inicio TEXT,
                    fecha_fin TEXT,
                    
                    -- Configuración específica por tipo (JSON)
                    dias_semana TEXT,
                    dias_mes TEXT,
                    intervalo_minutos INTEGER,
                    
                    -- Control de ejecución
                    ultima_ejecucion TEXT,
                    proxima_ejecucion TEXT,
                    total_ejecuciones INTEGER DEFAULT 0,
                    
                    -- Metadatos
                    fecha_creacion TEXT NOT NULL,
                    fecha_modificacion TEXT,
                    creado_por TEXT,
                    
                    FOREIGN KEY (control_id) REFERENCES controles (id)
                )
            """)
            
            # Crear índices para optimizar consultas
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_programaciones_control_id 
                ON programaciones(control_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_programaciones_activo 
                ON programaciones(activo)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_programaciones_proxima_ejecucion 
                ON programaciones(proxima_ejecucion)
            """)
    
    def crear(self, programacion: Programacion) -> Programacion:
        """Crea una nueva programación"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO programaciones (
                    control_id, nombre, descripcion, tipo_programacion, activo,
                    hora_ejecucion, fecha_inicio, fecha_fin,
                    dias_semana, dias_mes, intervalo_minutos,
                    ultima_ejecucion, proxima_ejecucion, total_ejecuciones,
                    fecha_creacion, fecha_modificacion, creado_por
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                programacion.control_id,
                programacion.nombre,
                programacion.descripcion,
                programacion.tipo_programacion.value,
                programacion.activo,
                self._time_to_string(programacion.hora_ejecucion),
                self._datetime_to_string(programacion.fecha_inicio),
                self._datetime_to_string(programacion.fecha_fin),
                self._dias_semana_to_json(programacion.dias_semana),
                self._dias_mes_to_json(programacion.dias_mes),
                programacion.intervalo_minutos,
                self._datetime_to_string(programacion.ultima_ejecucion),
                self._datetime_to_string(programacion.proxima_ejecucion),
                programacion.total_ejecuciones,
                self._datetime_to_string(programacion.fecha_creacion),
                self._datetime_to_string(programacion.fecha_modificacion),
                programacion.creado_por
            ))
            
            programacion.id = cursor.lastrowid
            return programacion
    
    def obtener_por_id(self, id: int) -> Optional[Programacion]:
        """Obtiene una programación por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM programaciones WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_programacion(row)
            return None
    
    def obtener_por_control_id(self, control_id: int) -> List[Programacion]:
        """Obtiene todas las programaciones de un control"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM programaciones WHERE control_id = ? ORDER BY nombre",
                (control_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_programacion(row) for row in rows]
    
    def obtener_todas(self) -> List[Programacion]:
        """Obtiene todas las programaciones"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM programaciones ORDER BY control_id, nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_programacion(row) for row in rows]
    
    def obtener_activas(self) -> List[Programacion]:
        """Obtiene todas las programaciones activas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM programaciones WHERE activo = 1 ORDER BY control_id, nombre"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_programacion(row) for row in rows]
    
    def obtener_pendientes_ejecucion(self, fecha_actual: datetime = None) -> List[Programacion]:
        """Obtiene las programaciones que deben ejecutarse ahora"""
        if fecha_actual is None:
            fecha_actual = datetime.now()
        
        # Obtener todas las programaciones activas y filtrar usando la lógica de la entidad
        programaciones_activas = self.obtener_activas()
        pendientes = []
        
        for programacion in programaciones_activas:
            if programacion.debe_ejecutarse_ahora(fecha_actual):
                pendientes.append(programacion)
        
        return pendientes
    
    def actualizar(self, programacion: Programacion) -> Programacion:
        """Actualiza una programación existente"""
        programacion.fecha_modificacion = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE programaciones SET
                    control_id = ?, nombre = ?, descripcion = ?, tipo_programacion = ?, activo = ?,
                    hora_ejecucion = ?, fecha_inicio = ?, fecha_fin = ?,
                    dias_semana = ?, dias_mes = ?, intervalo_minutos = ?,
                    ultima_ejecucion = ?, proxima_ejecucion = ?, total_ejecuciones = ?,
                    fecha_modificacion = ?, creado_por = ?
                WHERE id = ?
            """, (
                programacion.control_id,
                programacion.nombre,
                programacion.descripcion,
                programacion.tipo_programacion.value,
                programacion.activo,
                self._time_to_string(programacion.hora_ejecucion),
                self._datetime_to_string(programacion.fecha_inicio),
                self._datetime_to_string(programacion.fecha_fin),
                self._dias_semana_to_json(programacion.dias_semana),
                self._dias_mes_to_json(programacion.dias_mes),
                programacion.intervalo_minutos,
                self._datetime_to_string(programacion.ultima_ejecucion),
                self._datetime_to_string(programacion.proxima_ejecucion),
                programacion.total_ejecuciones,
                self._datetime_to_string(programacion.fecha_modificacion),
                programacion.creado_por,
                programacion.id
            ))
            
            return programacion
    
    def eliminar(self, id: int) -> bool:
        """Elimina una programación"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM programaciones WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def activar_desactivar(self, id: int, activo: bool) -> bool:
        """Activa o desactiva una programación"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE programaciones SET activo = ?, fecha_modificacion = ? WHERE id = ?",
                (activo, self._datetime_to_string(datetime.now()), id)
            )
            return cursor.rowcount > 0
    
    def marcar_ejecutada(self, id: int, fecha_ejecucion: datetime = None) -> bool:
        """Marca una programación como ejecutada"""
        if fecha_ejecucion is None:
            fecha_ejecucion = datetime.now()
        
        # Obtener la programación para actualizar sus contadores
        programacion = self.obtener_por_id(id)
        if not programacion:
            return False
        
        # Actualizar usando el método de la entidad
        programacion.marcar_ejecutado(fecha_ejecucion)
        
        # Guardar cambios
        self.actualizar(programacion)
        return True
    
    def obtener_historial_ejecuciones(self, control_id: int, limite: int = 50) -> List[dict]:
        """Obtiene el historial de ejecuciones programadas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT 
                    p.nombre as programacion_nombre,
                    p.ultima_ejecucion,
                    p.total_ejecuciones,
                    p.tipo_programacion
                FROM programaciones p
                WHERE p.control_id = ? AND p.ultima_ejecucion IS NOT NULL
                ORDER BY p.ultima_ejecucion DESC
                LIMIT ?
            """, (control_id, limite))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def obtener_estadisticas(self, control_id: int = None) -> dict:
        """Obtiene estadísticas de programaciones"""
        with sqlite3.connect(self.db_path) as conn:
            if control_id:
                # Estadísticas específicas del control
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_programaciones,
                        SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activas,
                        SUM(total_ejecuciones) as total_ejecuciones,
                        MAX(ultima_ejecucion) as ultima_ejecucion_general
                    FROM programaciones 
                    WHERE control_id = ?
                """, (control_id,))
            else:
                # Estadísticas globales
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_programaciones,
                        SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activas,
                        SUM(total_ejecuciones) as total_ejecuciones,
                        MAX(ultima_ejecucion) as ultima_ejecucion_general
                    FROM programaciones
                """)
            
            row = cursor.fetchone()
            return {
                'total_programaciones': row[0] or 0,
                'activas': row[1] or 0,
                'inactivas': (row[0] or 0) - (row[1] or 0),
                'total_ejecuciones': row[2] or 0,
                'ultima_ejecucion_general': row[3]
            }
    
    def _row_to_programacion(self, row) -> Programacion:
        """Convierte una fila de base de datos a entidad Programacion"""
        return Programacion(
            id=row['id'],
            control_id=row['control_id'],
            nombre=row['nombre'],
            descripcion=row['descripcion'],
            tipo_programacion=TipoProgramacion(row['tipo_programacion']),
            activo=bool(row['activo']),
            hora_ejecucion=self._string_to_time(row['hora_ejecucion']),
            fecha_inicio=self._string_to_datetime(row['fecha_inicio']),
            fecha_fin=self._string_to_datetime(row['fecha_fin']),
            dias_semana=self._json_to_dias_semana(row['dias_semana']),
            dias_mes=self._json_to_dias_mes(row['dias_mes']),
            intervalo_minutos=row['intervalo_minutos'],
            ultima_ejecucion=self._string_to_datetime(row['ultima_ejecucion']),
            proxima_ejecucion=self._string_to_datetime(row['proxima_ejecucion']),
            total_ejecuciones=row['total_ejecuciones'],
            fecha_creacion=self._string_to_datetime(row['fecha_creacion']),
            fecha_modificacion=self._string_to_datetime(row['fecha_modificacion']),
            creado_por=row['creado_por']
        )
    
    def _datetime_to_string(self, dt: Optional[datetime]) -> Optional[str]:
        """Convierte datetime a string ISO"""
        return dt.isoformat() if dt else None
    
    def _string_to_datetime(self, s: Optional[str]) -> Optional[datetime]:
        """Convierte string ISO a datetime"""
        return datetime.fromisoformat(s) if s else None
    
    def _time_to_string(self, t: Optional[time]) -> Optional[str]:
        """Convierte time a string"""
        return t.isoformat() if t else None
    
    def _string_to_time(self, s: Optional[str]) -> Optional[time]:
        """Convierte string a time"""
        return time.fromisoformat(s) if s else None
    
    def _dias_semana_to_json(self, dias: Optional[List[DiaSemana]]) -> Optional[str]:
        """Convierte lista de días de semana a JSON"""
        if dias:
            return json.dumps([dia.value for dia in dias])
        return None
    
    def _json_to_dias_semana(self, json_str: Optional[str]) -> Optional[List[DiaSemana]]:
        """Convierte JSON a lista de días de semana"""
        if json_str:
            valores = json.loads(json_str)
            return [DiaSemana(valor) for valor in valores]
        return None
    
    def _dias_mes_to_json(self, dias: Optional[List[int]]) -> Optional[str]:
        """Convierte lista de días del mes a JSON"""
        return json.dumps(dias) if dias else None
    
    def _json_to_dias_mes(self, json_str: Optional[str]) -> Optional[List[int]]:
        """Convierte JSON a lista de días del mes"""
        return json.loads(json_str) if json_str else None