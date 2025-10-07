"""
Caso de uso: Listar Asociaciones Consulta-Control

Este caso de uso maneja la obtención de asociaciones entre consultas y controles
"""
from typing import List
from src.domain.entities.consulta_control import ConsultaControl
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository


class ListarConsultaControlUseCase:
    """Caso de uso para listar asociaciones consulta-control"""
    
    def __init__(self, consulta_control_repository: ConsultaControlRepository):
        self._consulta_control_repository = consulta_control_repository
    
    def ejecutar_por_control(self, control_id: int) -> List[ConsultaControl]:
        """
        Obtiene todas las asociaciones de un control específico
        
        Args:
            control_id: ID del control
            
        Returns:
            List[ConsultaControl]: Lista de asociaciones del control
        """
        return self._consulta_control_repository.obtener_por_control(control_id)
    
    def ejecutar_por_consulta(self, consulta_id: int) -> List[ConsultaControl]:
        """
        Obtiene todas las asociaciones de una consulta específica
        
        Args:
            consulta_id: ID de la consulta
            
        Returns:
            List[ConsultaControl]: Lista de asociaciones de la consulta
        """
        return self._consulta_control_repository.obtener_por_consulta(consulta_id)
    
    def obtener_consulta_disparo(self, control_id: int) -> ConsultaControl:
        """
        Obtiene la consulta de disparo de un control
        
        Args:
            control_id: ID del control
            
        Returns:
            ConsultaControl: Asociación de la consulta de disparo o None
        """
        return self._consulta_control_repository.obtener_disparo_por_control(control_id)
    
    def ejecutar_todas(self) -> List[ConsultaControl]:
        """
        Obtiene todas las asociaciones
        
        Returns:
            List[ConsultaControl]: Lista de todas las asociaciones
        """
        return self._consulta_control_repository.obtener_todas()