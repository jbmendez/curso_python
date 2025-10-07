"""
Controlador para operaciones de Referentes

Este controlador maneja las operaciones CRUD de referentes
y sus asociaciones con controles
"""
from typing import Dict, Any, List, Optional
from src.application.use_cases.crear_referente_use_case import CrearReferenteUseCase
from src.application.use_cases.listar_referentes_use_case import ListarReferentesUseCase
from src.application.use_cases.actualizar_referente_use_case import ActualizarReferenteUseCase
from src.application.use_cases.eliminar_referente_use_case import EliminarReferenteUseCase
from src.application.dto.referente_dto import CrearReferenteDTO, ActualizarReferenteDTO
from src.domain.repositories.referente_repository import ReferenteRepository
from src.domain.repositories.control_referente_repository import ControlReferenteRepository


class ReferenteController:
    """Controlador de operaciones de referentes"""
    
    def __init__(
        self,
        crear_referente_use_case: CrearReferenteUseCase,
        listar_referentes_use_case: ListarReferentesUseCase,
        actualizar_referente_use_case: ActualizarReferenteUseCase,
        eliminar_referente_use_case: EliminarReferenteUseCase,
        referente_repository: ReferenteRepository,
        control_referente_repository: ControlReferenteRepository = None
    ):
        self._crear_referente_use_case = crear_referente_use_case
        self._listar_referentes_use_case = listar_referentes_use_case
        self._actualizar_referente_use_case = actualizar_referente_use_case
        self._eliminar_referente_use_case = eliminar_referente_use_case
        self._referente_repository = referente_repository
        self._control_referente_repository = control_referente_repository
    
    def crear_referente(
        self,
        nombre: str,
        email: str,
        path_archivos: str = "",
        activo: bool = True
    ) -> Dict[str, Any]:
        """
        Crea un nuevo referente
        
        Args:
            nombre: Nombre del referente
            email: Email del referente
            path_archivos: Ruta donde dejar archivos de reportes
            activo: Si el referente está activo
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            dto = CrearReferenteDTO(
                nombre=nombre,
                email=email,
                path_archivos=path_archivos,
                activo=activo
            )
            
            resultado = self._crear_referente_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "email": resultado.email,
                    "path_archivos": resultado.path_archivos,
                    "activo": resultado.activo
                },
                "status": 201,
                "message": f"Referente '{nombre}' creado exitosamente"
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "status": 400
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "status": 500
            }
    
    def obtener_todos(self, solo_activos: bool = False) -> Dict[str, Any]:
        """
        Obtiene todos los referentes
        
        Args:
            solo_activos: Si solo debe obtener referentes activos
            
        Returns:
            Dict con la lista de referentes
        """
        try:
            referentes = self._listar_referentes_use_case.ejecutar(solo_activos)
            
            return {
                "success": True,
                "data": [
                    {
                        "id": ref.id,
                        "nombre": ref.nombre,
                        "email": ref.email,
                        "path_archivos": ref.path_archivos,
                        "activo": ref.activo
                    }
                    for ref in referentes
                ],
                "status": 200,
                "message": f"Se encontraron {len(referentes)} referentes"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener referentes: {str(e)}",
                "status": 500
            }
    
    def obtener_por_id(self, referente_id: int) -> Dict[str, Any]:
        """
        Obtiene un referente por su ID
        
        Args:
            referente_id: ID del referente
            
        Returns:
            Dict con los datos del referente
        """
        try:
            referente = self._referente_repository.obtener_por_id(referente_id)
            
            if not referente:
                return {
                    "success": False,
                    "error": f"No se encontró el referente con ID {referente_id}",
                    "status": 404
                }
            
            return {
                "success": True,
                "data": {
                    "id": referente.id,
                    "nombre": referente.nombre,
                    "email": referente.email,
                    "path_archivos": referente.path_archivos,
                    "activo": referente.activo
                },
                "status": 200
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener referente: {str(e)}",
                "status": 500
            }
    
    def actualizar_referente(
        self,
        referente_id: int,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        path_archivos: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Actualiza un referente existente
        
        Args:
            referente_id: ID del referente a actualizar
            nombre: Nuevo nombre (opcional)
            email: Nuevo email (opcional)
            path_archivos: Nueva ruta de archivos (opcional)
            activo: Nuevo estado activo (opcional)
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            if self._actualizar_referente_use_case is None:
                return {
                    "success": False,
                    "error": "Funcionalidad de actualización no disponible",
                    "status": 501
                }
            
            dto = ActualizarReferenteDTO(
                nombre=nombre,
                email=email,
                path_archivos=path_archivos,
                activo=activo
            )
            
            resultado = self._actualizar_referente_use_case.ejecutar(referente_id, dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "email": resultado.email,
                    "path_archivos": resultado.path_archivos,
                    "activo": resultado.activo
                },
                "status": 200,
                "message": f"Referente actualizado exitosamente"
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "status": 400
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "status": 500
            }
    
    def eliminar_referente(self, referente_id: int) -> Dict[str, Any]:
        """
        Elimina un referente
        
        Args:
            referente_id: ID del referente a eliminar
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            eliminado = self._eliminar_referente_use_case.ejecutar(referente_id)
            
            if eliminado:
                return {
                    "success": True,
                    "status": 200,
                    "message": "Referente eliminado exitosamente"
                }
            else:
                return {
                    "success": False,
                    "error": "No se pudo eliminar el referente",
                    "status": 400
                }
                
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "status": 400
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "status": 500
            }
    
    def obtener_referentes_por_control(self, control_id: int) -> Dict[str, Any]:
        """
        Obtiene todos los referentes asociados a un control
        
        Args:
            control_id: ID del control
            
        Returns:
            Dict con la lista de referentes del control
        """
        try:
            if not self._control_referente_repository:
                return {
                    "success": False,
                    "error": "Funcionalidad de asociaciones no disponible",
                    "status": 501
                }
            
            asociaciones = self._control_referente_repository.obtener_por_control(control_id)
            referentes_ids = [asoc.referente_id for asoc in asociaciones if asoc.activa]
            
            if not referentes_ids:
                return {
                    "success": True,
                    "data": [],
                    "status": 200,
                    "message": "No se encontraron referentes para este control"
                }
            
            referentes = self._referente_repository.obtener_por_ids(referentes_ids)
            
            return {
                "success": True,
                "data": [
                    {
                        "id": ref.id,
                        "nombre": ref.nombre,
                        "email": ref.email,
                        "path_archivos": ref.path_archivos,
                        "activo": ref.activo
                    }
                    for ref in referentes
                ],
                "status": 200,
                "message": f"Se encontraron {len(referentes)} referentes para el control"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener referentes del control: {str(e)}",
                "status": 500
            }