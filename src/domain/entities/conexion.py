"""
Entidad Conexión

Representa una conexión a base de datos
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Conexion:
    """Entidad Conexión - Representa una conexión a base de datos"""
    
    id: Optional[int] = None
    nombre: str = ""
    base_datos: str = ""
    servidor: str = ""
    puerto: Optional[int] = None
    usuario: str = ""
    contraseña: str = ""
    tipo_motor: str = "postgresql"  # postgresql, mysql, sqlite, sqlserver, iseries
    driver_type: str = "default"  # Para IBM i: "odbc" o "jdbc", para otros: "default"
    activa: bool = True
    
    def es_configuracion_valida(self) -> bool:
        """Valida que la configuración de conexión sea correcta"""
        campos_obligatorios = [self.nombre, self.base_datos, self.servidor, self.usuario]
        return all(campo.strip() for campo in campos_obligatorios if isinstance(campo, str))
    
    def obtener_string_conexion(self) -> str:
        """Genera string de conexión según el tipo de motor"""
        if self.tipo_motor.lower() == "postgresql":
            puerto = self.puerto or 5432
            return f"postgresql://{self.usuario}:{self.contraseña}@{self.servidor}:{puerto}/{self.base_datos}"
        elif self.tipo_motor.lower() == "mysql":
            puerto = self.puerto or 3306
            return f"mysql://{self.usuario}:{self.contraseña}@{self.servidor}:{puerto}/{self.base_datos}"
        elif self.tipo_motor.lower() == "sqlite":
            # Para SQLite, manejar paths absolutos y relativos correctamente
            if self.base_datos.startswith('/'):
                return f"sqlite://{self.base_datos}"
            else:
                return f"sqlite:///{self.base_datos}"
        elif self.tipo_motor.lower() == "iseries":
            puerto = self.puerto or 446  # Puerto por defecto para iSeries
            return f"ibm_db_sa://{self.usuario}:{self.contraseña}@{self.servidor}:{puerto}/{self.base_datos}"
        elif self.tipo_motor.lower() == "sqlserver":
            puerto = self.puerto or 1433  # Puerto por defecto para SQL Server
            return f"mssql+pyodbc://{self.usuario}:{self.contraseña}@{self.servidor}:{puerto}/{self.base_datos}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            return ""
    
    def ocultar_contraseña(self) -> str:
        """Representa la conexión ocultando la contraseña"""
        return f"Conexion(nombre={self.nombre}, servidor={self.servidor}, bd={self.base_datos})"
    
    def __str__(self) -> str:
        return self.ocultar_contraseña()