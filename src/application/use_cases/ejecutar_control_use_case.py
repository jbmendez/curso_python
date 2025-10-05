"""
Caso de uso para ejecutar controles
"""
from typing import Optional
from datetime import datetime
from src.domain.repositories.control_repository import ControlRepository
from src.domain.repositories.conexion_repository import ConexionRepository
from src.domain.repositories.resultado_ejecucion_repository import ResultadoEjecucionRepository
from src.domain.services.ejecucion_control_service import EjecucionControlService
from src.application.dto.ejecucion_dto import EjecutarControlDTO, ResultadoEjecucionResponseDTO


class EjecutarControlUseCase:
    """Caso de uso para ejecutar un control específico"""
    
    def __init__(
        self,
        control_repository: ControlRepository,
        conexion_repository: ConexionRepository,
        resultado_repository: ResultadoEjecucionRepository,
        ejecucion_service: EjecucionControlService
    ):
        self.control_repository = control_repository
        self.conexion_repository = conexion_repository
        self.resultado_repository = resultado_repository
        self.ejecucion_service = ejecucion_service
    
    def ejecutar(self, dto: EjecutarControlDTO) -> ResultadoEjecucionResponseDTO:
        """
        Ejecuta un control específico
        
        Args:
            dto: Datos para la ejecución del control
            
        Returns:
            ResultadoEjecucionResponseDTO: Resultado de la ejecución
            
        Raises:
            ValueError: Si el control no existe o no está activo
        """
        # Obtener el control
        control = self.control_repository.obtener_por_id(dto.control_id)
        if not control:
            raise ValueError(f"Control con ID {dto.control_id} no encontrado")
        
        if not control.activo:
            raise ValueError(f"Control '{control.nombre}' está inactivo")
        
        # Obtener la conexión
        conexion = self.conexion_repository.obtener_por_id(control.conexion_id)
        if not conexion:
            raise ValueError(f"Conexión con ID {control.conexion_id} no encontrada")
        
        if not conexion.activa:
            raise ValueError(f"Conexión '{conexion.nombre}' está inactiva")
        
        # Ejecutar el control usando el servicio de dominio
        resultado = self.ejecucion_service.ejecutar_control(
            control=control,
            conexion=conexion,
            parametros_adicionales=dto.parametros_adicionales or {},
            ejecutar_solo_disparo=dto.ejecutar_solo_disparo,
            mock_execution=dto.mock_execution
        )
        
        # Guardar el resultado
        resultado_guardado = self.resultado_repository.guardar(resultado)
        
        # Convertir a DTO de respuesta
        return self._resultado_to_dto(resultado_guardado)
    
    def _resultado_to_dto(self, resultado) -> ResultadoEjecucionResponseDTO:
        """Convierte una entidad ResultadoEjecucion a DTO"""
        # Convertir resultado de consulta disparo a dict
        disparo_dict = None
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
        
        # Convertir resultados de consultas disparadas
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
            resultados_consultas_disparadas=disparadas_list if disparadas_list else None
        )