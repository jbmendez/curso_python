"""
Entidad Consulta

Representa una consulta SQL que puede ser ejecutada
"""
from dataclasses import dataclass
from typing import Optional, List
import re


@dataclass
class Consulta:
    """Entidad Consulta - Representa una consulta SQL"""
    
    id: Optional[int] = None
    nombre: str = ""
    sql: str = ""
    descripcion: str = ""
    control_id: Optional[int] = None
    conexion_id: Optional[int] = None
    activa: bool = True
    
    def es_sql_valido(self) -> bool:
        """Validación básica de SQL"""
        if not self.sql or not self.sql.strip():
            return False
        
        # Verificar que sea una sentencia SQL válida
        sql_upper = self.sql.upper().strip()
        
        # Permitir SELECT, WITH (CTE), EXPLAIN, SHOW, CALL, EXECUTE, etc.
        sentencias_validas = [
            'SELECT',      # Consultas básicas
            'WITH',        # Common Table Expressions (CTE)
            'EXPLAIN',     # Planes de ejecución
            'SHOW',        # Comandos SHOW (MySQL, etc.)
            'DESCRIBE',    # Describir estructura
            'DESC',        # Alias de DESCRIBE
            'PRAGMA',      # SQLite pragmas
            'CALL',        # Stored procedures (CALL procedimiento)
            'EXECUTE',     # Stored procedures (EXECUTE procedimiento)
            'EXEC'         # Alias de EXECUTE (SQL Server style)
        ]
        
        return any(sql_upper.startswith(sentencia) for sentencia in sentencias_validas)
    
    def es_valida(self) -> bool:
        """Validación general de la entidad"""
        return (self.nombre and self.nombre.strip() and 
                self.sql and self.sql.strip())
    
    def obtener_parametros_en_sql(self) -> List[str]:
        """Extrae los nombres de parámetros del SQL (formato :parametro)"""
        patron = r':(\w+)'
        return list(set(re.findall(patron, self.sql)))
    
    def es_consulta_peligrosa(self) -> bool:
        """Verifica si la consulta contiene operaciones peligrosas"""
        sql_upper = self.sql.upper()
        operaciones_peligrosas = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE', 'ALTER']
        return any(op in sql_upper for op in operaciones_peligrosas)
    
    def reemplazar_parametros(self, parametros: dict) -> str:
        """Reemplaza los parámetros en el SQL con sus valores"""
        sql_resultado = self.sql
        for nombre, valor in parametros.items():
            sql_resultado = sql_resultado.replace(f':{nombre}', str(valor))
        return sql_resultado
    
    def __str__(self) -> str:
        return f"Consulta(nombre={self.nombre}, activa={self.activa})"