"""
Controlador para operaciones de parámetros
"""
from typing import Dict, Any
from src.application.use_cases.crear_parametro_use_case import CrearParametroUseCase
from src.application.dto.parametro_dto import CrearParametroDTO


class ParametroController:
    """Controlador para endpoints de parámetros"""
    
    def __init__(self, crear_parametro_use_case: CrearParametroUseCase):
        self._crear_parametro_use_case = crear_parametro_use_case
    
    def crear_parametro(
        self,
        control_id: int,
        nombre: str,
        tipo: str,
        descripcion: str,
        valor_por_defecto: Any,
        obligatorio: bool = True
    ) -> Dict[str, Any]:
        """
        Crea un nuevo parámetro
        
        Args:
            control_id: ID del control al que pertenece
            nombre: Nombre del parámetro
            tipo: Tipo de dato del parámetro
            descripcion: Descripción del parámetro
            valor_por_defecto: Valor por defecto
            obligatorio: Si el parámetro es obligatorio
            
        Returns:
            dict: Respuesta con los datos del parámetro creado
        """
        try:
            dto = CrearParametroDTO(
                control_id=control_id,
                nombre=nombre,
                tipo=tipo,
                descripcion=descripcion,
                valor_por_defecto=valor_por_defecto,
                obligatorio=obligatorio
            )
            
            resultado = self._crear_parametro_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "nombre": resultado.nombre,
                    "tipo": resultado.tipo,
                    "descripcion": resultado.descripcion,
                    "valor_por_defecto": resultado.valor_por_defecto,
                    "obligatorio": resultado.obligatorio
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }