"""
Caso de uso: Listar Consultas

Este caso de uso maneja la obtención de consultas con filtros
"""
from typing import List, Optional
from src.domain.entities.consulta import Consulta
from src.domain.repositories.consulta_repository import ConsultaRepository


class ListarConsultasUseCase:
    """Caso de uso para listar consultas con filtros"""
    
    def __init__(self, consulta_repository: ConsultaRepository):
        self._consulta_repository = consulta_repository
    
    def ejecutar(
        self, 
        solo_activas: bool = False,
        control_id: Optional[int] = None
    ) -> List[Consulta]:
        """
        Ejecuta el caso de uso de listado de consultas
        
        Args:
            solo_activas: Si solo debe retornar consultas activas
            control_id: Filtrar por control específico
            
        Returns:
            List[Consulta]: Lista de consultas que cumplen los filtros
        """
        
        if control_id:
            # Filtrar por control
            consultas = self._consulta_repository.obtener_por_control(control_id)
        elif solo_activas:
            # Solo consultas activas
            consultas = self._consulta_repository.obtener_activas()
        else:
            # Todas las consultas
            consultas = self._consulta_repository.obtener_todos()
        
        # Aplicar filtro de activas si se especificó y no se usó el método obtener_activas
        if solo_activas and control_id:
            consultas = [c for c in consultas if c.activa]
        
        return consultas
    
    def obtener_por_ids(self, ids: List[int]) -> List[Consulta]:
        """Obtiene consultas específicas por sus IDs"""
        return self._consulta_repository.obtener_por_ids(ids)
    
    def obtener_por_id(self, consulta_id: int) -> Optional[Consulta]:
        """Obtiene una consulta específica por su ID"""
        return self._consulta_repository.obtener_por_id(consulta_id)