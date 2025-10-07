"""
Caso de uso: Actualizar Consulta

Este caso de uso maneja la actualización de consultas existentes
"""
from src.domain.entities.consulta import Consulta
from src.domain.repositories.consulta_repository import ConsultaRepository
from src.application.dto.consulta_dto import ActualizarConsultaDTO, ConsultaResponseDTO


class ActualizarConsultaUseCase:
    """Caso de uso para actualizar una consulta existente"""
    
    def __init__(self, consulta_repository: ConsultaRepository):
        self._consulta_repository = consulta_repository
    
    def ejecutar(self, consulta_id: int, datos: ActualizarConsultaDTO) -> ConsultaResponseDTO:
        """
        Ejecuta el caso de uso de actualización de consulta
        
        Args:
            consulta_id: ID de la consulta a actualizar
            datos: Datos para actualizar
            
        Returns:
            ConsultaResponseDTO: Datos de la consulta actualizada
            
        Raises:
            ValueError: Si la consulta no existe o hay errores de validación
        """
        
        # Obtener consulta existente
        consulta_existente = self._consulta_repository.obtener_por_id(consulta_id)
        if not consulta_existente:
            raise ValueError(f"No se encontró la consulta con ID {consulta_id}")
        
        # Verificar nombre único si se está cambiando
        if datos.nombre and datos.nombre != consulta_existente.nombre:
            consulta_con_nombre = self._consulta_repository.obtener_por_nombre(datos.nombre)
            if consulta_con_nombre and consulta_con_nombre.id != consulta_id:
                raise ValueError(f"Ya existe otra consulta con el nombre '{datos.nombre}'")
        
        # Crear consulta actualizada
        consulta_actualizada = Consulta(
            id=consulta_existente.id,
            nombre=datos.nombre if datos.nombre is not None else consulta_existente.nombre,
            sql=datos.sql if datos.sql is not None else consulta_existente.sql,
            descripcion=datos.descripcion if datos.descripcion is not None else consulta_existente.descripcion,
            control_id=consulta_existente.control_id,  # No se puede cambiar el control
            conexion_id=datos.conexion_id if datos.conexion_id is not None else consulta_existente.conexion_id,
            activa=datos.activa if datos.activa is not None else consulta_existente.activa
        )
        
        # Validaciones de negocio
        if not consulta_actualizada.es_valida():
            raise ValueError("Los datos de la consulta no son válidos")
        
        if not consulta_actualizada.es_sql_valido():
            raise ValueError("El SQL proporcionado no es válido")
        
        if consulta_actualizada.es_consulta_peligrosa():
            raise ValueError("La consulta contiene operaciones peligrosas (INSERT, UPDATE, DELETE, etc.)")
        
        # Guardar consulta actualizada
        consulta_guardada = self._consulta_repository.actualizar(consulta_actualizada)
        
        # Retornar DTO de respuesta
        return ConsultaResponseDTO(
            id=consulta_guardada.id,
            nombre=consulta_guardada.nombre,
            sql=consulta_guardada.sql,
            descripcion=consulta_guardada.descripcion,
            control_id=consulta_guardada.control_id,
            conexion_id=consulta_guardada.conexion_id,
            activa=consulta_guardada.activa
        )