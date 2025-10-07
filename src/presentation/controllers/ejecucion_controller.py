"""
Controlador para la ejecución de controles
"""
from typing import List, Optional
from datetime import datetime, timedelta
from src.application.use_cases.ejecutar_control_use_case import EjecutarControlUseCase
from src.application.use_cases.obtener_historial_ejecucion_use_case import ObtenerHistorialEjecucionUseCase
from src.application.dto.ejecucion_dto import (
    EjecutarControlDTO,
    ResultadoEjecucionResponseDTO,
    HistorialEjecucionDTO,
    EstadisticasEjecucionDTO,
    ResumenControlDTO
)


class EjecucionController:
    """Controlador para operaciones de ejecución de controles"""
    
    def __init__(
        self,
        ejecutar_use_case: EjecutarControlUseCase,
        historial_use_case: ObtenerHistorialEjecucionUseCase
    ):
        self.ejecutar_use_case = ejecutar_use_case
        self.historial_use_case = historial_use_case
    
    def ejecutar_control(
        self,
        control_id: int,
        ejecutar_solo_disparo: bool = False
    ) -> dict:
        """
        Ejecuta un control específico
        
        Args:
            control_id: ID del control a ejecutar
            ejecutar_solo_disparo: Si True, solo ejecuta la consulta de disparo
            
        Returns:
            dict: Resultado de la ejecución en formato JSON
        """
        try:
            dto = EjecutarControlDTO(
                control_id=control_id,
                parametros_adicionales=None,  # No implementado
                ejecutar_solo_disparo=ejecutar_solo_disparo,
                mock_execution=False  # No implementado
            )
            
            resultado = self.ejecutar_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "control_nombre": resultado.control_nombre,
                    "fecha_ejecucion": resultado.fecha_ejecucion.isoformat(),
                    "estado": resultado.estado,
                    "mensaje": resultado.mensaje,
                    "parametros_utilizados": resultado.parametros_utilizados,
                    "tiempo_total_ejecucion_ms": resultado.tiempo_total_ejecucion_ms,
                    "total_filas_disparo": resultado.total_filas_disparo,
                    "total_filas_disparadas": resultado.total_filas_disparadas,
                    "conexion_nombre": resultado.conexion_nombre,
                    "resultado_consulta_disparo": resultado.resultado_consulta_disparo,
                    "resultados_consultas_disparadas": resultado.resultados_consultas_disparadas
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_historial(
        self,
        control_id: int = None,
        fecha_desde: str = None,
        fecha_hasta: str = None,
        estado: str = None,
        limite: int = 50,
        incluir_detalles: bool = False
    ) -> dict:
        """
        Obtiene el historial de ejecuciones
        
        Args:
            control_id: ID del control (opcional)
            fecha_desde: Fecha de inicio en formato ISO (opcional)
            fecha_hasta: Fecha de fin en formato ISO (opcional)
            estado: Estado de ejecución (opcional)
            limite: Número máximo de resultados
            incluir_detalles: Si incluir detalles de consultas
            
        Returns:
            dict: Historial de ejecuciones en formato JSON
        """
        try:
            # Convertir fechas string a datetime
            fecha_desde_dt = None
            fecha_hasta_dt = None
            
            if fecha_desde:
                fecha_desde_dt = datetime.fromisoformat(fecha_desde.replace('Z', '+00:00'))
            if fecha_hasta:
                fecha_hasta_dt = datetime.fromisoformat(fecha_hasta.replace('Z', '+00:00'))
            
            dto = HistorialEjecucionDTO(
                control_id=control_id,
                fecha_desde=fecha_desde_dt,
                fecha_hasta=fecha_hasta_dt,
                estado=estado,
                limite=limite,
                incluir_detalles=incluir_detalles
            )
            
            resultados = self.historial_use_case.obtener_historial(dto)
            
            # Convertir resultados a formato JSON
            data = []
            for resultado in resultados:
                data.append({
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "control_nombre": resultado.control_nombre,
                    "fecha_ejecucion": resultado.fecha_ejecucion.isoformat(),
                    "estado": resultado.estado,
                    "mensaje": resultado.mensaje,
                    "parametros_utilizados": resultado.parametros_utilizados,
                    "tiempo_total_ejecucion_ms": resultado.tiempo_total_ejecucion_ms,
                    "total_filas_disparo": resultado.total_filas_disparo,
                    "total_filas_disparadas": resultado.total_filas_disparadas,
                    "conexion_nombre": resultado.conexion_nombre,
                    "resultado_consulta_disparo": resultado.resultado_consulta_disparo,
                    "resultados_consultas_disparadas": resultado.resultados_consultas_disparadas
                })
            
            return {
                "success": True,
                "data": data,
                "total": len(data)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_estadisticas(
        self,
        fecha_desde: str = None,
        fecha_hasta: str = None
    ) -> dict:
        """
        Obtiene estadísticas de ejecuciones
        
        Args:
            fecha_desde: Fecha de inicio en formato ISO (opcional)
            fecha_hasta: Fecha de fin en formato ISO (opcional)
            
        Returns:
            dict: Estadísticas en formato JSON
        """
        try:
            # Convertir fechas
            fecha_desde_dt = None
            fecha_hasta_dt = None
            
            if fecha_desde:
                fecha_desde_dt = datetime.fromisoformat(fecha_desde.replace('Z', '+00:00'))
            if fecha_hasta:
                fecha_hasta_dt = datetime.fromisoformat(fecha_hasta.replace('Z', '+00:00'))
            
            estadisticas = self.historial_use_case.obtener_estadisticas(
                fecha_desde_dt, fecha_hasta_dt
            )
            
            return {
                "success": True,
                "data": {
                    "total_ejecuciones": estadisticas.total_ejecuciones,
                    "ejecuciones_exitosas": estadisticas.ejecuciones_exitosas,
                    "ejecuciones_con_error": estadisticas.ejecuciones_con_error,
                    "controles_disparados": estadisticas.controles_disparados,
                    "sin_datos": estadisticas.sin_datos,
                    "tiempo_promedio_ejecucion_ms": estadisticas.tiempo_promedio_ejecucion_ms,
                    "tasa_exito": estadisticas.tasa_exito,
                    "ultima_ejecucion": estadisticas.ultima_ejecucion.isoformat() if estadisticas.ultima_ejecucion else None
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_resumen_controles(
        self,
        fecha_desde: str = None,
        fecha_hasta: str = None
    ) -> dict:
        """
        Obtiene resumen de ejecuciones por control
        
        Args:
            fecha_desde: Fecha de inicio en formato ISO (opcional)
            fecha_hasta: Fecha de fin en formato ISO (opcional)
            
        Returns:
            dict: Resumen por controles en formato JSON
        """
        try:
            # Convertir fechas
            fecha_desde_dt = None
            fecha_hasta_dt = None
            
            if fecha_desde:
                fecha_desde_dt = datetime.fromisoformat(fecha_desde.replace('Z', '+00:00'))
            if fecha_hasta:
                fecha_hasta_dt = datetime.fromisoformat(fecha_hasta.replace('Z', '+00:00'))
            
            resumenes = self.historial_use_case.obtener_resumen_por_control(
                fecha_desde_dt, fecha_hasta_dt
            )
            
            data = []
            for resumen in resumenes:
                data.append({
                    "control_id": resumen.control_id,
                    "control_nombre": resumen.control_nombre,
                    "total_ejecuciones": resumen.total_ejecuciones,
                    "ultima_ejecucion": resumen.ultima_ejecucion.isoformat() if resumen.ultima_ejecucion else None,
                    "ultimo_estado": resumen.ultimo_estado,
                    "tasa_exito": resumen.tasa_exito,
                    "tiempo_promedio_ms": resumen.tiempo_promedio_ms
                })
            
            return {
                "success": True,
                "data": data,
                "total": len(data)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_ultimos_resultados_control(
        self,
        control_id: int,
        limite: int = 10
    ) -> dict:
        """
        Obtiene los últimos resultados de un control específico
        
        Args:
            control_id: ID del control
            limite: Número máximo de resultados
            
        Returns:
            dict: Últimos resultados en formato JSON
        """
        try:
            resultados = self.historial_use_case.obtener_ultimos_por_control(
                control_id, limite
            )
            
            data = []
            for resultado in resultados:
                data.append({
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "control_nombre": resultado.control_nombre,
                    "fecha_ejecucion": resultado.fecha_ejecucion.isoformat(),
                    "estado": resultado.estado,
                    "mensaje": resultado.mensaje,
                    "parametros_utilizados": resultado.parametros_utilizados,
                    "tiempo_total_ejecucion_ms": resultado.tiempo_total_ejecucion_ms,
                    "total_filas_disparo": resultado.total_filas_disparo,
                    "total_filas_disparadas": resultado.total_filas_disparadas,
                    "conexion_nombre": resultado.conexion_nombre,
                    "resultado_consulta_disparo": resultado.resultado_consulta_disparo,
                    "resultados_consultas_disparadas": resultado.resultados_consultas_disparadas
                })
            
            return {
                "success": True,
                "data": data,
                "total": len(data)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }