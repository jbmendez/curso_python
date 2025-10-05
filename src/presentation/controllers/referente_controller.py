"""
Controlador para operaciones de referentes
"""
from typing import Dict, Any
from src.application.use_cases.crear_referente_use_case import CrearReferenteUseCase
from src.application.dto.referente_dto import CrearReferenteDTO


class ReferenteController:
    """Controlador para endpoints de referentes"""
    
    def __init__(self, crear_referente_use_case: CrearReferenteUseCase):
        self._crear_referente_use_case = crear_referente_use_case
    
    def crear_referente(
        self,
        control_id: int,
        nombre: str,
        email: str,
        cargo: str
    ) -> Dict[str, Any]:
        """
        Crea un nuevo referente
        
        Args:
            control_id: ID del control al que pertenece
            nombre: Nombre del referente
            email: Email del referente
            cargo: Cargo del referente
            
        Returns:
            dict: Respuesta con los datos del referente creado
        """
        try:
            dto = CrearReferenteDTO(
                control_id=control_id,
                nombre=nombre,
                email=email,
                cargo=cargo
            )
            
            resultado = self._crear_referente_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "nombre": resultado.nombre,
                    "email": resultado.email,
                    "cargo": resultado.cargo
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }