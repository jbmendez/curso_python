"""
Caso de uso para actualizar conexiones existentes
"""
from src.domain.entities.conexion import Conexion
from src.domain.repositories.conexion_repository import ConexionRepository
from src.application.dto.conexion_dto import CrearConexionDTO


class ActualizarConexionUseCase:
    """Caso de uso para actualizar una conexión existente"""
    
    def __init__(self, conexion_repository: ConexionRepository):
        self._conexion_repository = conexion_repository
    
    def ejecutar(self, conexion_id: int, dto: CrearConexionDTO) -> Conexion:
        """
        Actualiza una conexión existente
        
        Args:
            conexion_id: ID de la conexión a actualizar
            dto: Datos actualizados de la conexión
            
        Returns:
            Conexion: La conexión actualizada
            
        Raises:
            ValueError: Si la conexión no existe o los datos son inválidos
        """
        # Verificar que la conexión existe
        conexion_existente = self._conexion_repository.obtener_por_id(conexion_id)
        if not conexion_existente:
            raise ValueError(f"No se encontró la conexión con ID {conexion_id}")
        
        # Si la contraseña es el marcador especial, mantener la contraseña actual
        password_final = dto.password
        if dto.password == "***KEEP_CURRENT***":
            password_final = conexion_existente.contraseña
        
        # Crear la conexión actualizada
        conexion_actualizada = Conexion(
            id=conexion_id,
            nombre=dto.nombre,
            base_datos=dto.base_datos,
            servidor=dto.servidor,
            puerto=dto.puerto,
            usuario=dto.usuario,
            contraseña=password_final,
            tipo_motor=dto.motor,
            activa=dto.activa  # Usar el valor del DTO
        )
        
        # Validar los datos
        if not conexion_actualizada.es_configuracion_valida():
            raise ValueError("Los datos de la conexión no son válidos")
        
        # Guardar la conexión actualizada
        return self._conexion_repository.guardar(conexion_actualizada)