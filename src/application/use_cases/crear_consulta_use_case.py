"""
Caso de uso: Crear Consulta

Este caso de uso maneja la creación de una nueva consulta SQL
"""
from src.domain.entities.consulta import Consulta
from src.domain.repositories.consulta_repository import ConsultaRepository
from src.application.dto.consulta_dto import CrearConsultaDTO, ConsultaResponseDTO


class CrearConsultaUseCase:
    """Caso de uso para crear una nueva consulta"""
    
    def __init__(self, consulta_repository: ConsultaRepository):
        self._consulta_repository = consulta_repository
    
    def ejecutar(self, datos: CrearConsultaDTO) -> ConsultaResponseDTO:
        """Ejecuta el caso de uso de creación de consulta"""
        
        # Verificar que el nombre no exista
        consulta_existente = self._consulta_repository.obtener_por_nombre(datos.nombre)
        if consulta_existente:
            raise ValueError(f"Ya existe una consulta con el nombre '{datos.nombre}'")
        
        # Crear entidad consulta
        consulta = Consulta(
            nombre=datos.nombre,
            sql=datos.sql,
            descripcion=datos.descripcion,
            control_id=datos.control_id,
            conexion_id=datos.conexion_id,
            activa=datos.activa
        )
        
        # Validaciones de negocio
        if not consulta.es_valida():
            raise ValueError("Los datos de la consulta no son válidos")
        
        if not consulta.es_sql_valido():
            raise ValueError("El SQL proporcionado no es válido")
        
        if consulta.es_consulta_peligrosa():
            raise ValueError("La consulta contiene operaciones peligrosas (INSERT, UPDATE, DELETE, etc.)")
        
        # Guardar consulta
        consulta_guardada = self._consulta_repository.guardar(consulta)
        
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