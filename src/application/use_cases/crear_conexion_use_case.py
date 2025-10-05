"""
Caso de uso para crear conexiones
"""
from src.domain.entities.conexion import Conexion
from src.domain.repositories.conexion_repository import ConexionRepository
from src.application.dto.conexion_dto import CrearConexionDTO, ConexionResponseDTO


class CrearConexionUseCase:
    """Caso de uso para crear una nueva conexión"""
    
    def __init__(self, conexion_repository: ConexionRepository):
        self._conexion_repository = conexion_repository
    
    def ejecutar(self, datos: CrearConexionDTO) -> ConexionResponseDTO:
        """Ejecuta el caso de uso de creación de conexión"""
        
        # Verificar que no exista otra conexión con el mismo nombre
        conexiones_existentes = self._conexion_repository.obtener_todos()
        if any(c.nombre.lower() == datos.nombre.lower() for c in conexiones_existentes):
            raise ValueError(f"Ya existe una conexión con el nombre '{datos.nombre}'")
        
        # Crear entidad conexión
        conexion = Conexion(
            id=None,
            nombre=datos.nombre,
            tipo_motor=datos.motor,
            servidor=datos.servidor,
            puerto=datos.puerto,
            base_datos=datos.base_datos,
            usuario=datos.usuario,
            contraseña=datos.password,
            activa=True
        )
        
        # Guardar conexión
        conexion_guardada = self._conexion_repository.guardar(conexion)
        
        # Retornar DTO de respuesta
        return ConexionResponseDTO(
            id=conexion_guardada.id,
            nombre=conexion_guardada.nombre,
            motor=conexion_guardada.tipo_motor,
            servidor=conexion_guardada.servidor,
            puerto=conexion_guardada.puerto,
            base_datos=conexion_guardada.base_datos,
            usuario=conexion_guardada.usuario,
            activa=conexion_guardada.activa
        )