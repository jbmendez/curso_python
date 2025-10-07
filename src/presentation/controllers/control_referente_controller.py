"""
Controlador para las asociaciones Control-Referente

Este controlador maneja las operaciones de asociación
entre controles y referentes
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.domain.repositories.control_referente_repository import ControlReferenteRepository
from src.domain.repositories.control_repository import ControlRepository
from src.domain.repositories.referente_repository import ReferenteRepository
from src.domain.entities.control_referente import ControlReferente


class ControlReferenteController:
    """Controlador de asociaciones Control-Referente"""
    
    def __init__(
        self,
        control_referente_repository: ControlReferenteRepository,
        control_repository: ControlRepository,
        referente_repository: ReferenteRepository
    ):
        self._control_referente_repository = control_referente_repository
        self._control_repository = control_repository
        self._referente_repository = referente_repository
    
    def asociar_control_referente(
        self,
        control_id: int,
        referente_id: int,
        notificar_por_email: bool = True,
        notificar_por_archivo: bool = False,
        observaciones: str = ""
    ) -> Dict[str, Any]:
        """
        Asocia un control con un referente
        
        Args:
            control_id: ID del control
            referente_id: ID del referente
            notificar_por_email: Si debe notificar por email
            notificar_por_archivo: Si debe notificar por archivo
            observaciones: Observaciones de la asociación
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            # Verificar que el control existe
            control = self._control_repository.obtener_por_id(control_id)
            if not control:
                return {
                    "success": False,
                    "error": f"No se encontró el control con ID {control_id}",
                    "status": 404
                }
            
            # Verificar que el referente existe
            referente = self._referente_repository.obtener_por_id(referente_id)
            if not referente:
                return {
                    "success": False,
                    "error": f"No se encontró el referente con ID {referente_id}",
                    "status": 404
                }
            
            # Verificar si ya existe la asociación
            if self._control_referente_repository.existe_asociacion(control_id, referente_id):
                return {
                    "success": False,
                    "error": "Ya existe una asociación entre este control y referente",
                    "status": 409
                }
            
            # Crear la asociación
            asociacion = ControlReferente(
                control_id=control_id,
                referente_id=referente_id,
                activa=True,
                fecha_asociacion=datetime.now(),
                notificar_por_email=notificar_por_email,
                notificar_por_archivo=notificar_por_archivo,
                observaciones=observaciones
            )
            
            id_asociacion = self._control_referente_repository.guardar(asociacion)
            
            return {
                "success": True,
                "data": {
                    "id": id_asociacion,
                    "control_id": control_id,
                    "control_nombre": control.nombre,
                    "referente_id": referente_id,
                    "referente_nombre": referente.nombre,
                    "referente_email": referente.email,
                    "activa": True,
                    "fecha_asociacion": asociacion.fecha_asociacion.isoformat(),
                    "notificar_por_email": notificar_por_email,
                    "notificar_por_archivo": notificar_por_archivo,
                    "observaciones": observaciones
                },
                "status": 201,
                "message": f"Asociación creada entre control '{control.nombre}' y referente '{referente.nombre}'"
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
    
    def obtener_asociaciones_control(self, control_id: int) -> Dict[str, Any]:
        """
        Obtiene todas las asociaciones de un control
        
        Args:
            control_id: ID del control
            
        Returns:
            Dict con la lista de asociaciones del control
        """
        try:
            # Verificar que el control existe
            control = self._control_repository.obtener_por_id(control_id)
            if not control:
                return {
                    "success": False,
                    "error": f"No se encontró el control con ID {control_id}",
                    "status": 404
                }
            
            asociaciones = self._control_referente_repository.obtener_por_control(control_id)
            
            # Obtener información de los referentes
            resultado = []
            for asociacion in asociaciones:
                referente = self._referente_repository.obtener_por_id(asociacion.referente_id)
                if referente:
                    resultado.append({
                        "id": asociacion.id,
                        "control_id": control_id,
                        "control_nombre": control.nombre,
                        "referente_id": referente.id,
                        "referente_nombre": referente.nombre,
                        "referente_email": referente.email,
                        "referente_path_archivos": referente.path_archivos,
                        "activa": asociacion.activa,
                        "fecha_asociacion": asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else None,
                        "notificar_por_email": asociacion.notificar_por_email,
                        "notificar_por_archivo": asociacion.notificar_por_archivo,
                        "observaciones": asociacion.observaciones
                    })
            
            return {
                "success": True,
                "data": resultado,
                "status": 200,
                "message": f"Se encontraron {len(resultado)} asociaciones para el control '{control.nombre}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener asociaciones: {str(e)}",
                "status": 500
            }
    
    def obtener_asociaciones_referente(self, referente_id: int) -> Dict[str, Any]:
        """
        Obtiene todas las asociaciones de un referente
        
        Args:
            referente_id: ID del referente
            
        Returns:
            Dict con la lista de asociaciones del referente
        """
        try:
            # Verificar que el referente existe
            referente = self._referente_repository.obtener_por_id(referente_id)
            if not referente:
                return {
                    "success": False,
                    "error": f"No se encontró el referente con ID {referente_id}",
                    "status": 404
                }
            
            asociaciones = self._control_referente_repository.obtener_por_referente(referente_id)
            
            # Obtener información de los controles
            resultado = []
            for asociacion in asociaciones:
                control = self._control_repository.obtener_por_id(asociacion.control_id)
                if control:
                    resultado.append({
                        "id": asociacion.id,
                        "control_id": control.id,
                        "control_nombre": control.nombre,
                        "control_descripcion": control.descripcion,
                        "referente_id": referente_id,
                        "referente_nombre": referente.nombre,
                        "activa": asociacion.activa,
                        "fecha_asociacion": asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else None,
                        "notificar_por_email": asociacion.notificar_por_email,
                        "notificar_por_archivo": asociacion.notificar_por_archivo,
                        "observaciones": asociacion.observaciones
                    })
            
            return {
                "success": True,
                "data": resultado,
                "status": 200,
                "message": f"Se encontraron {len(resultado)} asociaciones para el referente '{referente.nombre}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener asociaciones: {str(e)}",
                "status": 500
            }
    
    def obtener_asociacion_por_id(self, asociacion_id: int) -> Dict[str, Any]:
        """
        Obtiene una asociación específica por su ID
        
        Args:
            asociacion_id: ID de la asociación
            
        Returns:
            Dict con los datos de la asociación
        """
        try:
            asociacion = self._control_referente_repository.obtener_por_id(asociacion_id)
            if not asociacion:
                return {
                    "success": False,
                    "error": f"No se encontró la asociación con ID {asociacion_id}",
                    "status": 404
                }
            
            # Obtener información del control y referente
            control = self._control_repository.obtener_por_id(asociacion.control_id)
            referente = self._referente_repository.obtener_por_id(asociacion.referente_id)
            
            return {
                "success": True,
                "data": {
                    "id": asociacion.id,
                    "control_id": asociacion.control_id,
                    "control_nombre": control.nombre if control else "N/A",
                    "referente_id": asociacion.referente_id,
                    "referente_nombre": referente.nombre if referente else "N/A",
                    "activa": asociacion.activa,
                    "fecha_asociacion": asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else None,
                    "notificar_por_email": asociacion.notificar_por_email,
                    "notificar_por_archivo": asociacion.notificar_por_archivo,
                    "observaciones": asociacion.observaciones or ""
                },
                "status": 200,
                "message": "Asociación encontrada exitosamente"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener asociación: {str(e)}",
                "status": 500
            }

    def actualizar_asociacion(
        self,
        asociacion_id: int,
        activa: Optional[bool] = None,
        notificar_por_email: Optional[bool] = None,
        notificar_por_archivo: Optional[bool] = None,
        observaciones: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Actualiza una asociación existente
        
        Args:
            asociacion_id: ID de la asociación
            activa: Nuevo estado activo (opcional)
            notificar_por_email: Nueva configuración de notificación por email (opcional)
            notificar_por_archivo: Nueva configuración de notificación por archivo (opcional)
            observaciones: Nuevas observaciones (opcional)
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            # Obtener la asociación actual
            asociacion = self._control_referente_repository.obtener_por_id(asociacion_id)
            if not asociacion:
                return {
                    "success": False,
                    "error": f"No se encontró la asociación con ID {asociacion_id}",
                    "status": 404
                }
            
            # Actualizar solo los campos proporcionados
            if activa is not None:
                asociacion.activa = activa
            if notificar_por_email is not None:
                asociacion.notificar_por_email = notificar_por_email
            if notificar_por_archivo is not None:
                asociacion.notificar_por_archivo = notificar_por_archivo
            if observaciones is not None:
                asociacion.observaciones = observaciones
            
            # Validar la asociación actualizada
            if not asociacion.es_valida():
                return {
                    "success": False,
                    "error": "Los datos de la asociación no son válidos",
                    "status": 400
                }
            
            # Guardar los cambios
            self._control_referente_repository.guardar(asociacion)
            
            # Obtener información completa para la respuesta
            control = self._control_repository.obtener_por_id(asociacion.control_id)
            referente = self._referente_repository.obtener_por_id(asociacion.referente_id)
            
            return {
                "success": True,
                "data": {
                    "id": asociacion.id,
                    "control_id": asociacion.control_id,
                    "control_nombre": control.nombre if control else "N/A",
                    "referente_id": asociacion.referente_id,
                    "referente_nombre": referente.nombre if referente else "N/A",
                    "activa": asociacion.activa,
                    "fecha_asociacion": asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else None,
                    "notificar_por_email": asociacion.notificar_por_email,
                    "notificar_por_archivo": asociacion.notificar_por_archivo,
                    "observaciones": asociacion.observaciones
                },
                "status": 200,
                "message": "Asociación actualizada exitosamente"
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
    
    def eliminar_asociacion(self, control_id: int, referente_id: int) -> Dict[str, Any]:
        """
        Elimina una asociación entre control y referente
        
        Args:
            control_id: ID del control
            referente_id: ID del referente
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            eliminado = self._control_referente_repository.eliminar_por_control_referente(
                control_id, 
                referente_id
            )
            
            if eliminado:
                return {
                    "success": True,
                    "status": 200,
                    "message": "Asociación eliminada exitosamente"
                }
            else:
                return {
                    "success": False,
                    "error": "No se encontró la asociación a eliminar",
                    "status": 404
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "status": 500
            }
    
    def eliminar_asociacion_por_id(self, asociacion_id: int) -> Dict[str, Any]:
        """
        Elimina una asociación por su ID
        
        Args:
            asociacion_id: ID de la asociación
            
        Returns:
            Dict con respuesta de la operación
        """
        try:
            eliminado = self._control_referente_repository.eliminar(asociacion_id)
            
            if eliminado:
                return {
                    "success": True,
                    "status": 200,
                    "message": "Asociación eliminada exitosamente"
                }
            else:
                return {
                    "success": False,
                    "error": "No se encontró la asociación a eliminar",
                    "status": 404
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "status": 500
            }