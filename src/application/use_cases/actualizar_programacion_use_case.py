"""
Caso de uso para actualizar programación

Maneja la actualización de programaciones existentes
con validación de reglas de negocio.
"""
from ...domain.repositories.programacion_repository import ProgramacionRepository
from ...domain.entities.programacion import Programacion
from ..dto.programacion_dto import ActualizarProgramacionDTO


class ActualizarProgramacionUseCase:
    """Caso de uso para actualizar una programación existente"""
    
    def __init__(self, programacion_repository: ProgramacionRepository):
        self.programacion_repository = programacion_repository
    
    def ejecutar(self, dto: ActualizarProgramacionDTO) -> Programacion:
        """
        Actualiza una programación existente
        
        Args:
            dto: Datos actualizados de la programación
            
        Returns:
            Programacion: Programación actualizada
            
        Raises:
            ValueError: Si la programación no existe o los datos son inválidos
        """
        # Verificar que la programación existe
        programacion_existente = self.programacion_repository.obtener_por_id(dto.id)
        if not programacion_existente:
            raise ValueError(f"La programación con ID {dto.id} no existe")
        
        # Actualizar campos
        programacion_existente.nombre = dto.nombre
        programacion_existente.descripcion = dto.descripcion
        programacion_existente.tipo_programacion = dto.tipo_programacion
        programacion_existente.activo = dto.activo
        programacion_existente.hora_ejecucion = dto.hora_ejecucion
        programacion_existente.fecha_inicio = dto.fecha_inicio
        programacion_existente.fecha_fin = dto.fecha_fin
        programacion_existente.dias_semana = dto.dias_semana
        programacion_existente.dias_mes = dto.dias_mes
        programacion_existente.intervalo_minutos = dto.intervalo_minutos
        
        # Validar la programación actualizada
        if not programacion_existente.es_valida():
            raise ValueError("La configuración de programación actualizada no es válida")
        
        # Validar nombre único para el control (excluyendo la programación actual)
        programaciones_control = self.programacion_repository.obtener_por_control_id(
            programacion_existente.control_id
        )
        nombres_existentes = [
            p.nombre.lower() for p in programaciones_control 
            if p.id != dto.id
        ]
        if dto.nombre.lower() in nombres_existentes:
            raise ValueError(f"Ya existe otra programación con el nombre '{dto.nombre}' para este control")
        
        # Recalcular próxima ejecución
        programacion_existente._calcular_proxima_ejecucion()
        
        # Actualizar en repositorio
        return self.programacion_repository.actualizar(programacion_existente)