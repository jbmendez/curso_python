"""
Implementación concreta del repositorio de ResultadoEjecucion usando SQLite
"""
import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from src.domain.entities.resultado_ejecucion import ResultadoEjecucion, ResultadoConsulta, EstadoEjecucion
from src.domain.repositories.resultado_ejecucion_repository import ResultadoEjecucionRepository


class SQLiteResultadoEjecucionRepository(ResultadoEjecucionRepository):
    """Implementación del repositorio de resultados usando SQLite"""
    
    def __init__(self, db_path: str = "controles.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea la tabla de resultados si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resultados_ejecucion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    control_id INTEGER NOT NULL,
                    control_nombre TEXT NOT NULL,
                    fecha_ejecucion TIMESTAMP NOT NULL,
                    estado TEXT NOT NULL,
                    mensaje TEXT,
                    parametros_utilizados TEXT,  -- JSON
                    resultado_consulta_disparo TEXT,  -- JSON
                    resultados_consultas_disparadas TEXT,  -- JSON array
                    tiempo_total_ejecucion_ms REAL,
                    total_filas_disparo INTEGER,
                    total_filas_disparadas INTEGER,
                    conexion_id INTEGER,
                    conexion_nombre TEXT
                )
            """)
            
            # Crear índices para mejorar performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_control_id ON resultados_ejecucion(control_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fecha_ejecucion ON resultados_ejecucion(fecha_ejecucion)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_estado ON resultados_ejecucion(estado)")
    
    def obtener_por_id(self, id: int) -> Optional[ResultadoEjecucion]:
        """Obtiene un resultado por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM resultados_ejecucion WHERE id = ?", (id,)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_resultado(row)
            return None
    
    def obtener_todos(self) -> List[ResultadoEjecucion]:
        """Obtiene todos los resultados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM resultados_ejecucion ORDER BY fecha_ejecucion DESC"
            )
            rows = cursor.fetchall()
            
            return [self._row_to_resultado(row) for row in rows]
    
    def obtener_por_control(self, control_id: int) -> List[ResultadoEjecucion]:
        """Obtiene todos los resultados de un control específico"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM resultados_ejecucion 
                   WHERE control_id = ? 
                   ORDER BY fecha_ejecucion DESC""",
                (control_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_resultado(row) for row in rows]
    
    def obtener_por_fecha_rango(
        self, 
        fecha_desde: datetime, 
        fecha_hasta: datetime
    ) -> List[ResultadoEjecucion]:
        """Obtiene resultados en un rango de fechas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM resultados_ejecucion 
                   WHERE fecha_ejecucion BETWEEN ? AND ?
                   ORDER BY fecha_ejecucion DESC""",
                (fecha_desde.isoformat(), fecha_hasta.isoformat())
            )
            rows = cursor.fetchall()
            
            return [self._row_to_resultado(row) for row in rows]
    
    def obtener_por_estado(self, estado: str) -> List[ResultadoEjecucion]:
        """Obtiene resultados por estado"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM resultados_ejecucion 
                   WHERE estado = ?
                   ORDER BY fecha_ejecucion DESC""",
                (estado,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_resultado(row) for row in rows]
    
    def guardar(self, resultado: ResultadoEjecucion) -> ResultadoEjecucion:
        """Guarda un resultado de ejecución"""
        with sqlite3.connect(self.db_path) as conn:
            if resultado.id is None:
                # Crear nuevo resultado
                cursor = conn.execute(
                    """INSERT INTO resultados_ejecucion 
                       (control_id, control_nombre, fecha_ejecucion, estado, mensaje,
                        parametros_utilizados, resultado_consulta_disparo, 
                        resultados_consultas_disparadas, tiempo_total_ejecucion_ms,
                        total_filas_disparo, total_filas_disparadas, conexion_id, conexion_nombre)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        resultado.control_id,
                        resultado.control_nombre,
                        resultado.fecha_ejecucion.isoformat() if resultado.fecha_ejecucion else None,
                        resultado.estado.value,
                        resultado.mensaje,
                        json.dumps(resultado.parametros_utilizados),
                        json.dumps(self._consulta_to_dict(resultado.resultado_consulta_disparo)),
                        json.dumps([self._consulta_to_dict(c) for c in resultado.resultados_consultas_disparadas]),
                        resultado.tiempo_total_ejecucion_ms,
                        resultado.total_filas_disparo,
                        resultado.total_filas_disparadas,
                        resultado.conexion_id,
                        resultado.conexion_nombre
                    )
                )
                resultado.id = cursor.lastrowid
            
            return resultado
    
    def eliminar(self, id: int) -> bool:
        """Elimina un resultado por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM resultados_ejecucion WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def obtener_ultimos_por_control(self, control_id: int, limite: int = 10) -> List[ResultadoEjecucion]:
        """Obtiene los últimos N resultados de un control"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM resultados_ejecucion 
                   WHERE control_id = ?
                   ORDER BY fecha_ejecucion DESC
                   LIMIT ?""",
                (control_id, limite)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_resultado(row) for row in rows]
    
    def _row_to_resultado(self, row: sqlite3.Row) -> ResultadoEjecucion:
        """Convierte una fila de base de datos a una entidad ResultadoEjecucion"""
        # Deserializar JSONs
        parametros = json.loads(row['parametros_utilizados']) if row['parametros_utilizados'] else {}
        
        resultado_disparo_dict = json.loads(row['resultado_consulta_disparo']) if row['resultado_consulta_disparo'] else None
        resultado_disparo = self._dict_to_consulta(resultado_disparo_dict) if resultado_disparo_dict else None
        
        resultados_disparadas = []
        if row['resultados_consultas_disparadas']:
            disparadas_list = json.loads(row['resultados_consultas_disparadas'])
            resultados_disparadas = [self._dict_to_consulta(d) for d in disparadas_list if d]
        
        return ResultadoEjecucion(
            id=row['id'],
            control_id=row['control_id'],
            control_nombre=row['control_nombre'],
            fecha_ejecucion=datetime.fromisoformat(row['fecha_ejecucion']) if row['fecha_ejecucion'] else None,
            estado=EstadoEjecucion(row['estado']),
            mensaje=row['mensaje'] or "",
            parametros_utilizados=parametros,
            resultado_consulta_disparo=resultado_disparo,
            resultados_consultas_disparadas=resultados_disparadas,
            tiempo_total_ejecucion_ms=row['tiempo_total_ejecucion_ms'] or 0.0,
            total_filas_disparo=row['total_filas_disparo'] or 0,
            total_filas_disparadas=row['total_filas_disparadas'] or 0,
            conexion_id=row['conexion_id'] or 0,
            conexion_nombre=row['conexion_nombre'] or ""
        )
    
    def _consulta_to_dict(self, consulta: Optional[ResultadoConsulta]) -> Optional[dict]:
        """Convierte ResultadoConsulta a diccionario para JSON"""
        if not consulta:
            return None
        
        return {
            'consulta_id': consulta.consulta_id,
            'consulta_nombre': consulta.consulta_nombre,
            'sql_ejecutado': consulta.sql_ejecutado,
            'filas_afectadas': consulta.filas_afectadas,
            'datos': consulta.datos,
            'tiempo_ejecucion_ms': consulta.tiempo_ejecucion_ms,
            'error': consulta.error
        }
    
    def _dict_to_consulta(self, data: dict) -> ResultadoConsulta:
        """Convierte diccionario a ResultadoConsulta"""
        return ResultadoConsulta(
            consulta_id=data.get('consulta_id', 0),
            consulta_nombre=data.get('consulta_nombre', ''),
            sql_ejecutado=data.get('sql_ejecutado', ''),
            filas_afectadas=data.get('filas_afectadas', 0),
            datos=data.get('datos', []),
            tiempo_ejecucion_ms=data.get('tiempo_ejecucion_ms', 0.0),
            error=data.get('error')
        )