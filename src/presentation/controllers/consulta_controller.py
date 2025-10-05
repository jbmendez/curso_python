"""
Controlador para operaciones de consultas
"""
from typing import Dict, Any
from src.application.use_cases.crear_consulta_use_case import CrearConsultaUseCase
from src.application.dto.consulta_dto import CrearConsultaDTO


class ConsultaController:
    """Controlador para endpoints de consultas"""
    
    def __init__(self, crear_consulta_use_case: CrearConsultaUseCase):
        self._crear_consulta_use_case = crear_consulta_use_case
    
    def crear_consulta(
        self,
        control_id: int,
        nombre: str,
        sql: str,
        tipo: str,
        activa: bool = True
    ) -> Dict[str, Any]:
        """
        Crea una nueva consulta
        
        Args:
            control_id: ID del control al que pertenece
            nombre: Nombre de la consulta
            sql: Código SQL de la consulta
            tipo: Tipo de consulta (disparo, disparada)
            activa: Si la consulta está activa
            
        Returns:
            dict: Respuesta con los datos de la consulta creada
        """
        try:
            dto = CrearConsultaDTO(
                control_id=control_id,
                nombre=nombre,
                sql=sql,
                tipo=tipo,
                activa=activa
            )
            
            resultado = self._crear_consulta_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "nombre": resultado.nombre,
                    "sql": resultado.sql,
                    "tipo": resultado.tipo,
                    "activa": resultado.activa
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }