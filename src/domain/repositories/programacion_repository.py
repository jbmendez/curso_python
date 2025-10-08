"""
Repositorio abstracto para gestión de programaciones de controles

Define la interfaz para operaciones CRUD de programaciones
y consultas específicas para el sistema de ejecución automática.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities.programacion import Programacion


class ProgramacionRepository(ABC):
    """Repositorio abstracto para gestión de programaciones"""
    
    @abstractmethod
    def crear(self, programacion: Programacion) -> Programacion:
        """
        Crea una nueva programación
        
        Args:
            programacion: Programación a crear
            
        Returns:
            Programacion: Programación creada con ID asignado
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Programacion]:
        """
        Obtiene una programación por su ID
        
        Args:
            id: ID de la programación
            
        Returns:
            Optional[Programacion]: Programación encontrada o None
        """
        pass
    
    @abstractmethod
    def obtener_por_control_id(self, control_id: int) -> List[Programacion]:
        """
        Obtiene todas las programaciones de un control específico
        
        Args:
            control_id: ID del control
            
        Returns:
            List[Programacion]: Lista de programaciones del control
        """
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[Programacion]:
        """
        Obtiene todas las programaciones
        
        Returns:
            List[Programacion]: Lista de todas las programaciones
        """
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Programacion]:
        """
        Obtiene todas las programaciones activas
        
        Returns:
            List[Programacion]: Lista de programaciones activas
        """
        pass
    
    @abstractmethod
    def obtener_pendientes_ejecucion(self, fecha_actual: datetime = None) -> List[Programacion]:
        """
        Obtiene las programaciones que deben ejecutarse ahora
        
        Args:
            fecha_actual: Fecha/hora actual (por defecto datetime.now())
            
        Returns:
            List[Programacion]: Lista de programaciones a ejecutar
        """
        pass
    
    @abstractmethod
    def actualizar(self, programacion: Programacion) -> Programacion:
        """
        Actualiza una programación existente
        
        Args:
            programacion: Programación con datos actualizados
            
        Returns:
            Programacion: Programación actualizada
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina una programación
        
        Args:
            id: ID de la programación a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def activar_desactivar(self, id: int, activo: bool) -> bool:
        """
        Activa o desactiva una programación
        
        Args:
            id: ID de la programación
            activo: True para activar, False para desactivar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pass
    
    @abstractmethod
    def marcar_ejecutada(self, id: int, fecha_ejecucion: datetime = None) -> bool:
        """
        Marca una programación como ejecutada
        
        Args:
            id: ID de la programación
            fecha_ejecucion: Fecha de ejecución (por defecto datetime.now())
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pass
    
    @abstractmethod
    def obtener_historial_ejecuciones(self, control_id: int, limite: int = 50) -> List[dict]:
        """
        Obtiene el historial de ejecuciones programadas de un control
        
        Args:
            control_id: ID del control
            limite: Número máximo de registros a retornar
            
        Returns:
            List[dict]: Lista de ejecuciones con fecha, resultado, etc.
        """
        pass
    
    @abstractmethod
    def obtener_estadisticas(self, control_id: int = None) -> dict:
        """
        Obtiene estadísticas de programaciones
        
        Args:
            control_id: ID del control (opcional, si no se especifica retorna globales)
            
        Returns:
            dict: Estadísticas como total_programaciones, activas, ejecuciones_hoy, etc.
        """
        pass