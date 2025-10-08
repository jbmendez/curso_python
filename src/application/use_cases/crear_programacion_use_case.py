"""
Caso de uso para crear programación

Maneja la creación de nuevas programaciones de controles
con validación de reglas de negocio.
"""
from datetime import datetime
from typing import Optional

from ...domain.entities.programacion import Programacion
from ...domain.repositories.programacion_repository import ProgramacionRepository
from ...domain.repositories.control_repository import ControlRepository
from ..dto.programacion_dto import CrearProgramacionDTO


class CrearProgramacionUseCase:
    """Caso de uso para crear una nueva programación"""
    
    def __init__(
        self, 
        programacion_repository: ProgramacionRepository,
        control_repository: ControlRepository
    ):
        self.programacion_repository = programacion_repository
        self.control_repository = control_repository
    
    def ejecutar(self, dto: CrearProgramacionDTO) -> Programacion:
        """
        Crea una nueva programación
        
        Args:
            dto: Datos para crear la programación
            
        Returns:
            Programacion: Programación creada
            
        Raises:
            ValueError: Si los datos son inválidos o el control no existe
        """
        # Validar que el control existe
        control = self.control_repository.obtener_por_id(dto.control_id)
        if not control:
            raise ValueError(f"El control con ID {dto.control_id} no existe")
        
        # Crear la entidad programación
        programacion = Programacion(
            id=None,
            control_id=dto.control_id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            tipo_programacion=dto.tipo_programacion,
            activo=dto.activo,
            hora_ejecucion=dto.hora_ejecucion,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            dias_semana=dto.dias_semana,
            dias_mes=dto.dias_mes,
            intervalo_minutos=dto.intervalo_minutos,
            ultima_ejecucion=None,
            proxima_ejecucion=None,
            total_ejecuciones=0,
            fecha_creacion=datetime.now(),
            creado_por=dto.creado_por
        )
        
        # Validar la programación
        if not programacion.es_valida():
            raise ValueError("La configuración de programación no es válida")
        
        # Validar que no exista otra programación con el mismo nombre para el control
        programaciones_existentes = self.programacion_repository.obtener_por_control_id(dto.control_id)
        if any(p.nombre.lower() == dto.nombre.lower() for p in programaciones_existentes):
            raise ValueError(f"Ya existe una programación con el nombre '{dto.nombre}' para este control")
        
        # Calcular próxima ejecución
        programacion._calcular_proxima_ejecucion()
        
        # Crear en repositorio
        return self.programacion_repository.crear(programacion)