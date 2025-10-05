"""
Caso de uso para obtener el historial de ejecuciones
"""
from typing import List
from datetime import datetime, timedelta
from src.domain.repositories.resultado_ejecucion_repository import ResultadoEjecucionRepository
from src.domain.repositories.control_repository import ControlRepository
from src.application.dto.ejecucion_dto import (
    HistorialEjecucionDTO, 
    ResultadoEjecucionResponseDTO,
    EstadisticasEjecucionDTO,
    ResumenControlDTO
)


class ObtenerHistorialEjecucionUseCase:
    """Caso de uso para obtener historial y estadísticas de ejecuciones"""
    
    def __init__(
        self,
        resultado_repository: ResultadoEjecucionRepository,
        control_repository: ControlRepository
    ):
        self.resultado_repository = resultado_repository
        self.control_repository = control_repository
    
    def obtener_historial(self, dto: HistorialEjecucionDTO) -> List[ResultadoEjecucionResponseDTO]:
        """
        Obtiene el historial de ejecuciones según los filtros especificados
        
        Args:
            dto: Filtros para el historial
            
        Returns:
            List[ResultadoEjecucionResponseDTO]: Lista de resultados
        """
        resultados = []
        
        if dto.control_id:
            # Obtener por control específico
            resultados = self.resultado_repository.obtener_por_control(dto.control_id)
        elif dto.fecha_desde and dto.fecha_hasta:
            # Obtener por rango de fechas
            resultados = self.resultado_repository.obtener_por_fecha_rango(
                dto.fecha_desde, 
                dto.fecha_hasta
            )
        elif dto.estado:
            # Obtener por estado
            resultados = self.resultado_repository.obtener_por_estado(dto.estado)
        else:
            # Obtener todos
            resultados = self.resultado_repository.obtener_todos()
        
        # Aplicar límite
        if dto.limite > 0:
            resultados = resultados[:dto.limite]
        
        # Convertir a DTOs
        return [self._resultado_to_dto(resultado, dto.incluir_detalles) for resultado in resultados]
    
    def obtener_estadisticas(
        self, 
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> EstadisticasEjecucionDTO:
        """
        Obtiene estadísticas generales de ejecuciones
        
        Args:
            fecha_desde: Fecha de inicio para las estadísticas
            fecha_hasta: Fecha de fin para las estadísticas
            
        Returns:
            EstadisticasEjecucionDTO: Estadísticas de ejecución
        """
        if not fecha_desde:
            fecha_desde = datetime.now() - timedelta(days=30)  # Últimos 30 días por defecto
        if not fecha_hasta:
            fecha_hasta = datetime.now()
        
        resultados = self.resultado_repository.obtener_por_fecha_rango(fecha_desde, fecha_hasta)
        
        total = len(resultados)
        exitosos = len([r for r in resultados if r.estado.value == "EXITOSO"])
        errores = len([r for r in resultados if r.estado.value == "ERROR"])
        disparados = len([r for r in resultados if r.estado.value == "CONTROL_DISPARADO"])
        sin_datos = len([r for r in resultados if r.estado.value == "SIN_DATOS"])
        
        # Calcular tiempo promedio
        tiempos = [r.tiempo_total_ejecucion_ms for r in resultados if r.tiempo_total_ejecucion_ms > 0]
        tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0
        
        # Última ejecución
        ultima = max([r.fecha_ejecucion for r in resultados]) if resultados else None
        
        return EstadisticasEjecucionDTO(
            total_ejecuciones=total,
            ejecuciones_exitosas=exitosos,
            ejecuciones_con_error=errores,
            controles_disparados=disparados,
            sin_datos=sin_datos,
            tiempo_promedio_ejecucion_ms=tiempo_promedio,
            ultima_ejecucion=ultima
        )
    
    def obtener_resumen_por_control(
        self,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> List[ResumenControlDTO]:
        """
        Obtiene un resumen de ejecuciones agrupado por control
        
        Args:
            fecha_desde: Fecha de inicio
            fecha_hasta: Fecha de fin
            
        Returns:
            List[ResumenControlDTO]: Resumen por cada control
        """
        if not fecha_desde:
            fecha_desde = datetime.now() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = datetime.now()
        
        resultados = self.resultado_repository.obtener_por_fecha_rango(fecha_desde, fecha_hasta)
        
        # Agrupar por control
        controles_data = {}
        for resultado in resultados:
            control_id = resultado.control_id
            if control_id not in controles_data:
                controles_data[control_id] = {
                    'nombre': resultado.control_nombre,
                    'resultados': []
                }
            controles_data[control_id]['resultados'].append(resultado)
        
        # Generar resúmenes
        resumenes = []
        for control_id, data in controles_data.items():
            resultados_control = data['resultados']
            total = len(resultados_control)
            exitosos = len([r for r in resultados_control if r.estado.value == "EXITOSO"])
            
            # Última ejecución
            ultima = max([r.fecha_ejecucion for r in resultados_control])
            ultimo_estado = next(r.estado.value for r in resultados_control if r.fecha_ejecucion == ultima)
            
            # Tiempo promedio
            tiempos = [r.tiempo_total_ejecucion_ms for r in resultados_control if r.tiempo_total_ejecucion_ms > 0]
            tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0
            
            # Tasa de éxito
            tasa_exito = (exitosos / total * 100) if total > 0 else 0.0
            
            resumenes.append(ResumenControlDTO(
                control_id=control_id,
                control_nombre=data['nombre'],
                total_ejecuciones=total,
                ultima_ejecucion=ultima,
                ultimo_estado=ultimo_estado,
                tasa_exito=tasa_exito,
                tiempo_promedio_ms=tiempo_promedio
            ))
        
        # Ordenar por última ejecución (más reciente primero)
        resumenes.sort(key=lambda x: x.ultima_ejecucion or datetime.min, reverse=True)
        
        return resumenes
    
    def obtener_ultimos_por_control(self, control_id: int, limite: int = 10) -> List[ResultadoEjecucionResponseDTO]:
        """
        Obtiene los últimos resultados de un control específico
        
        Args:
            control_id: ID del control
            limite: Número máximo de resultados
            
        Returns:
            List[ResultadoEjecucionResponseDTO]: Últimos resultados
        """
        resultados = self.resultado_repository.obtener_ultimos_por_control(control_id, limite)
        return [self._resultado_to_dto(resultado, True) for resultado in resultados]
    
    def _resultado_to_dto(self, resultado, incluir_detalles: bool = False) -> ResultadoEjecucionResponseDTO:
        """Convierte una entidad ResultadoEjecucion a DTO"""
        disparo_dict = None
        disparadas_list = None
        
        if incluir_detalles:
            # Incluir detalles de consultas
            if resultado.resultado_consulta_disparo:
                disparo_dict = {
                    'consulta_id': resultado.resultado_consulta_disparo.consulta_id,
                    'consulta_nombre': resultado.resultado_consulta_disparo.consulta_nombre,
                    'sql_ejecutado': resultado.resultado_consulta_disparo.sql_ejecutado,
                    'filas_afectadas': resultado.resultado_consulta_disparo.filas_afectadas,
                    'datos': resultado.resultado_consulta_disparo.datos,
                    'tiempo_ejecucion_ms': resultado.resultado_consulta_disparo.tiempo_ejecucion_ms,
                    'error': resultado.resultado_consulta_disparo.error
                }
            
            if resultado.resultados_consultas_disparadas:
                disparadas_list = []
                for consulta in resultado.resultados_consultas_disparadas:
                    disparadas_list.append({
                        'consulta_id': consulta.consulta_id,
                        'consulta_nombre': consulta.consulta_nombre,
                        'sql_ejecutado': consulta.sql_ejecutado,
                        'filas_afectadas': consulta.filas_afectadas,
                        'datos': consulta.datos,
                        'tiempo_ejecucion_ms': consulta.tiempo_ejecucion_ms,
                        'error': consulta.error
                    })
        
        return ResultadoEjecucionResponseDTO(
            id=resultado.id,
            control_id=resultado.control_id,
            control_nombre=resultado.control_nombre,
            fecha_ejecucion=resultado.fecha_ejecucion,
            estado=resultado.estado.value,
            mensaje=resultado.mensaje,
            parametros_utilizados=resultado.parametros_utilizados,
            tiempo_total_ejecucion_ms=resultado.tiempo_total_ejecucion_ms,
            total_filas_disparo=resultado.total_filas_disparo,
            total_filas_disparadas=resultado.total_filas_disparadas,
            conexion_nombre=resultado.conexion_nombre,
            resultado_consulta_disparo=disparo_dict,
            resultados_consultas_disparadas=disparadas_list
        )