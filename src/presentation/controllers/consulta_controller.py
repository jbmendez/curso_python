"""
Controlador para operaciones de consultas
"""
from typing import Dict, Any, List, Optional
from src.application.use_cases.crear_consulta_use_case import CrearConsultaUseCase
from src.application.use_cases.listar_consultas_use_case import ListarConsultasUseCase
from src.application.use_cases.actualizar_consulta_use_case import ActualizarConsultaUseCase
from src.application.use_cases.eliminar_consulta_use_case import EliminarConsultaUseCase
from src.application.dto.consulta_dto import CrearConsultaDTO, ActualizarConsultaDTO


class ConsultaController:
    """Controlador para endpoints de consultas"""
    
    def __init__(
        self, 
        crear_consulta_use_case: CrearConsultaUseCase,
        listar_consultas_use_case: ListarConsultasUseCase,
        actualizar_consulta_use_case: ActualizarConsultaUseCase = None,
        eliminar_consulta_use_case: EliminarConsultaUseCase = None
    ):
        self._crear_consulta_use_case = crear_consulta_use_case
        self._listar_consultas_use_case = listar_consultas_use_case
        self._actualizar_consulta_use_case = actualizar_consulta_use_case
        self._eliminar_consulta_use_case = eliminar_consulta_use_case
    
    def crear_consulta(
        self,
        nombre: str,
        sql: str,
        descripcion: str = "",
        control_id: Optional[int] = None,
        conexion_id: Optional[int] = None,
        activa: bool = True
    ) -> Dict[str, Any]:
        """
        Crea una nueva consulta
        
        Args:
            nombre: Nombre de la consulta
            sql: Código SQL de la consulta
            descripcion: Descripción de la consulta
            control_id: ID del control al que pertenece (opcional)
            conexion_id: ID de la conexión específica (opcional)
            activa: Si la consulta está activa
            
        Returns:
            dict: Respuesta con los datos de la consulta creada
        """
        try:
            dto = CrearConsultaDTO(
                nombre=nombre,
                sql=sql,
                descripcion=descripcion,
                control_id=control_id,
                conexion_id=conexion_id,
                activa=activa
            )
            
            resultado = self._crear_consulta_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "sql": resultado.sql,
                    "descripcion": resultado.descripcion,
                    "control_id": resultado.control_id,
                    "conexion_id": resultado.conexion_id,
                    "activa": resultado.activa
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_todas(
        self, 
        solo_activas: bool = False,
        control_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene todas las consultas con filtros opcionales
        
        Args:
            solo_activas: Si solo debe retornar consultas activas
            control_id: Filtrar por control específico
            
        Returns:
            dict: Respuesta con la lista de consultas
        """
        try:
            consultas = self._listar_consultas_use_case.ejecutar(
                solo_activas=solo_activas,
                control_id=control_id
            )
            
            consultas_data = []
            for consulta in consultas:
                consulta_data = {
                    'id': consulta.id,
                    'nombre': consulta.nombre,
                    'sql': consulta.sql,
                    'descripcion': consulta.descripcion,
                    'control_id': consulta.control_id,
                    'conexion_id': consulta.conexion_id,
                    'activa': consulta.activa
                }
                consultas_data.append(consulta_data)
            
            return {
                'success': True,
                'data': consultas_data,
                'status': 200,
                'message': f'Se encontraron {len(consultas_data)} consultas'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 500
            }
    
    def obtener_por_id(self, consulta_id: int) -> Dict[str, Any]:
        """
        Obtiene una consulta específica por su ID
        
        Args:
            consulta_id: ID de la consulta
            
        Returns:
            dict: Respuesta con los datos de la consulta
        """
        try:
            consulta = self._listar_consultas_use_case.obtener_por_id(consulta_id)
            
            if not consulta:
                return {
                    "success": False,
                    "error": f"No se encontró la consulta con ID {consulta_id}",
                    "status": 404
                }
            
            return {
                "success": True,
                "data": {
                    "id": consulta.id,
                    "nombre": consulta.nombre,
                    "sql": consulta.sql,
                    "descripcion": consulta.descripcion,
                    "control_id": consulta.control_id,
                    "conexion_id": consulta.conexion_id,
                    "activa": consulta.activa
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def actualizar_consulta(
        self,
        consulta_id: int,
        nombre: Optional[str] = None,
        sql: Optional[str] = None,
        descripcion: Optional[str] = None,
        conexion_id: Optional[int] = None,
        activa: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Actualiza una consulta existente
        
        Args:
            consulta_id: ID de la consulta a actualizar
            nombre: Nuevo nombre (opcional)
            sql: Nuevo SQL (opcional)
            descripcion: Nueva descripción (opcional)
            conexion_id: Nueva conexión ID (opcional)
            activa: Nuevo estado activo (opcional)
            
        Returns:
            dict: Respuesta con los datos de la consulta actualizada
        """
        try:
            if self._actualizar_consulta_use_case is None:
                return {
                    "success": False,
                    "error": "Funcionalidad de actualización no disponible"
                }
            
            dto = ActualizarConsultaDTO(
                nombre=nombre,
                sql=sql,
                descripcion=descripcion,
                conexion_id=conexion_id,
                activa=activa
            )
            
            resultado = self._actualizar_consulta_use_case.ejecutar(consulta_id, dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "sql": resultado.sql,
                    "descripcion": resultado.descripcion,
                    "control_id": resultado.control_id,
                    "conexion_id": resultado.conexion_id,
                    "activa": resultado.activa
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def eliminar_consulta(self, consulta_id: int) -> Dict[str, Any]:
        """
        Elimina una consulta existente
        
        Args:
            consulta_id: ID de la consulta a eliminar
            
        Returns:
            dict: Respuesta con el resultado de la eliminación
        """
        try:
            if self._eliminar_consulta_use_case is None:
                return {
                    "success": False,
                    "error": "Funcionalidad de eliminación no disponible"
                }
            
            resultado = self._eliminar_consulta_use_case.ejecutar(consulta_id)
            
            return {
                "success": True,
                "message": f"Consulta con ID {consulta_id} eliminada exitosamente"
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}"
            }
    
    def desactivar_consulta(self, consulta_id: int) -> Dict[str, Any]:
        """
        Desactiva una consulta en lugar de eliminarla
        
        Args:
            consulta_id: ID de la consulta a desactivar
            
        Returns:
            dict: Respuesta con el resultado de la desactivación
        """
        try:
            if self._eliminar_consulta_use_case is None:
                return {
                    "success": False,
                    "error": "Funcionalidad de desactivación no disponible"
                }
            
            resultado = self._eliminar_consulta_use_case.desactivar(consulta_id)
            
            return {
                "success": True,
                "message": f"Consulta con ID {consulta_id} desactivada exitosamente"
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno: {str(e)}"
            }