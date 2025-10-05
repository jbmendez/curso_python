"""
Servicio de dominio para la ejecución de controles SQL

Este servicio contiene la lógica de negocio para ejecutar controles
sobre las bases de datos objetivo.
"""
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.domain.entities.control import Control
from src.domain.entities.conexion import Conexion
from src.domain.entities.consulta import Consulta
from src.domain.entities.resultado_ejecucion import ResultadoEjecucion, ResultadoConsulta, EstadoEjecucion
from src.domain.repositories.control_repository import ControlRepository
from src.domain.repositories.parametro_repository import ParametroRepository
from src.domain.repositories.consulta_repository import ConsultaRepository
from src.domain.repositories.referente_repository import ReferenteRepository
from src.domain.repositories.conexion_repository import ConexionRepository


class EjecucionControlService:
    """Servicio de dominio para ejecutar controles SQL"""
    
    def __init__(
        self,
        control_repository: ControlRepository,
        parametro_repository: ParametroRepository,
        consulta_repository: ConsultaRepository,
        referente_repository: ReferenteRepository,
        conexion_repository: ConexionRepository
    ):
        self._control_repository = control_repository
        self._parametro_repository = parametro_repository
        self._consulta_repository = consulta_repository
        self._referente_repository = referente_repository
        self._conexion_repository = conexion_repository
    
    def ejecutar_control(
        self,
        control: Control,
        conexion: Conexion,
        parametros_adicionales: Dict[str, Any] = None,
        ejecutar_solo_disparo: bool = False,
        mock_execution: bool = False
    ) -> ResultadoEjecucion:
        """
        Ejecuta un control específico
        
        Args:
            control: Control a ejecutar
            conexion: Conexión a la base de datos
            parametros_adicionales: Parámetros adicionales para la ejecución
            ejecutar_solo_disparo: Si True, solo ejecuta la consulta de disparo
            mock_execution: Si True, simula la ejecución (para testing)
            
        Returns:
            ResultadoEjecucion: Resultado de la ejecución
        """
        inicio_tiempo = time.time()
        
        try:
            # Obtener parámetros del control
            parametros = self._parametro_repository.obtener_por_control(control.id)
            
            # Combinar parámetros por defecto con adicionales
            valores_parametros = {}
            for param in parametros:
                valores_parametros[param.nombre] = param.valor_por_defecto
            
            if parametros_adicionales:
                valores_parametros.update(parametros_adicionales)
            
            # Obtener consultas
            consultas = self._consulta_repository.obtener_por_control(control.id)
            consulta_disparo = next((c for c in consultas if c.tipo == "disparo"), None)
            consultas_disparadas = [c for c in consultas if c.tipo == "disparada"]
            
            if not consulta_disparo:
                return self._crear_resultado_error(
                    control, conexion, valores_parametros, 
                    "No se encontró consulta de disparo para el control"
                )
            
            # Ejecutar consulta de disparo
            resultado_disparo = self._ejecutar_consulta(
                consulta_disparo, valores_parametros, conexion, mock_execution
            )
            
            if resultado_disparo.error:
                return self._crear_resultado_error(
                    control, conexion, valores_parametros,
                    f"Error en consulta de disparo: {resultado_disparo.error}",
                    resultado_disparo
                )
            
            # Evaluar si el control se dispara
            filas_disparo = resultado_disparo.filas_afectadas
            control_se_dispara = filas_disparo > 0
            
            resultados_disparadas = []
            total_filas_disparadas = 0
            
            # Si el control se dispara y no es solo disparo, ejecutar consultas disparadas
            if control_se_dispara and not ejecutar_solo_disparo and consultas_disparadas:
                for consulta in consultas_disparadas:
                    resultado = self._ejecutar_consulta(
                        consulta, valores_parametros, conexion, mock_execution
                    )
                    resultados_disparadas.append(resultado)
                    if not resultado.error:
                        total_filas_disparadas += resultado.filas_afectadas
            
            # Determinar estado final
            estado = self._determinar_estado(control_se_dispara, filas_disparo, resultados_disparadas)
            
            # Crear mensaje
            mensaje = self._crear_mensaje(estado, filas_disparo, total_filas_disparadas, ejecutar_solo_disparo)
            
            tiempo_total = (time.time() - inicio_tiempo) * 1000  # en millisegundos
            
            return ResultadoEjecucion(
                id=None,
                control_id=control.id,
                control_nombre=control.nombre,
                fecha_ejecucion=datetime.now(),
                estado=estado,
                mensaje=mensaje,
                parametros_utilizados=valores_parametros,
                resultado_consulta_disparo=resultado_disparo,
                resultados_consultas_disparadas=resultados_disparadas,
                tiempo_total_ejecucion_ms=tiempo_total,
                total_filas_disparo=filas_disparo,
                total_filas_disparadas=total_filas_disparadas,
                conexion_id=conexion.id,
                conexion_nombre=conexion.nombre
            )
            
        except Exception as e:
            tiempo_total = (time.time() - inicio_tiempo) * 1000
            return self._crear_resultado_error(
                control, conexion, parametros_adicionales or {},
                f"Error inesperado durante la ejecución: {str(e)}",
                tiempo_total=tiempo_total
            )
    
    def _ejecutar_consulta(
        self,
        consulta: Consulta,
        parametros: Dict[str, Any],
        conexion: Conexion,
        mock_execution: bool = False
    ) -> ResultadoConsulta:
        """Ejecuta una consulta específica"""
        inicio = time.time()
        
        try:
            if mock_execution:
                # Simular ejecución para demo/testing
                return self._simular_ejecucion_consulta(consulta, parametros)
            else:
                # Aquí iría la lógica real de conexión a la base de datos
                # Por ahora simulamos
                return self._simular_ejecucion_consulta(consulta, parametros)
                
        except Exception as e:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=self._reemplazar_parametros(consulta.sql, parametros),
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=str(e)
            )
    
    def _simular_ejecucion_consulta(self, consulta: Consulta, parametros: Dict[str, Any]) -> ResultadoConsulta:
        """Simula la ejecución de una consulta para demo/testing"""
        sql_ejecutado = self._reemplazar_parametros(consulta.sql, parametros)
        
        # Simular tiempo de ejecución
        tiempo_simulado = random.uniform(10, 100)  # Entre 10ms y 100ms
        
        # Simular resultados según el tipo de consulta
        if consulta.tipo == "disparo":
            # Para consultas de disparo, simular que a veces se dispara
            filas = random.choice([0, 0, 0, 1, 2, 5, 10])  # Más probabilidad de 0
            datos = [{"total": filas}] if filas > 0 else []
        else:
            # Para consultas disparadas, simular datos de ejemplo
            filas = random.randint(1, 20)
            datos = [
                {
                    "id": i,
                    "campo_ejemplo": f"valor_{i}",
                    "monto": random.randint(1000, 50000)
                }
                for i in range(min(filas, 5))  # Máximo 5 filas de ejemplo
            ]
        
        return ResultadoConsulta(
            consulta_id=consulta.id,
            consulta_nombre=consulta.nombre,
            sql_ejecutado=sql_ejecutado,
            filas_afectadas=filas,
            datos=datos,
            tiempo_ejecucion_ms=tiempo_simulado,
            error=None
        )
    
    def _reemplazar_parametros(self, sql: str, parametros: Dict[str, Any]) -> str:
        """Reemplaza parámetros en el SQL (simulación)"""
        sql_final = sql
        for nombre, valor in parametros.items():
            placeholder = f":{nombre}"
            sql_final = sql_final.replace(placeholder, str(valor))
        return sql_final
    
    def _determinar_estado(
        self, 
        control_se_dispara: bool, 
        filas_disparo: int, 
        resultados_disparadas: List[ResultadoConsulta]
    ) -> EstadoEjecucion:
        """Determina el estado final del control"""
        # Si hay errores en consultas disparadas
        if any(r.error for r in resultados_disparadas):
            return EstadoEjecucion.ERROR
        
        # Si no se dispara
        if not control_se_dispara or filas_disparo == 0:
            return EstadoEjecucion.SIN_DATOS
        
        # Si se dispara
        if control_se_dispara:
            return EstadoEjecucion.CONTROL_DISPARADO
        
        # Ejecución exitosa sin disparo
        return EstadoEjecucion.EXITOSO
    
    def _crear_mensaje(
        self, 
        estado: EstadoEjecucion, 
        filas_disparo: int, 
        total_filas_disparadas: int,
        ejecutar_solo_disparo: bool
    ) -> str:
        """Crea el mensaje descriptivo del resultado"""
        if estado == EstadoEjecucion.ERROR:
            return "Error durante la ejecución del control"
        elif estado == EstadoEjecucion.SIN_DATOS:
            return f"Control ejecutado exitosamente. No se encontraron datos ({filas_disparo} filas)"
        elif estado == EstadoEjecucion.CONTROL_DISPARADO:
            if ejecutar_solo_disparo:
                return f"Consulta de disparo ejecutada: {filas_disparo} filas encontradas"
            else:
                return f"Control disparado: {filas_disparo} filas de disparo, {total_filas_disparadas} filas procesadas"
        else:
            return "Control ejecutado exitosamente"
    
    def _crear_resultado_error(
        self,
        control: Control,
        conexion: Conexion,
        parametros: Dict[str, Any],
        mensaje: str,
        resultado_disparo: ResultadoConsulta = None,
        tiempo_total: float = 0.0
    ) -> ResultadoEjecucion:
        """Crea un resultado de error"""
        return ResultadoEjecucion(
            id=None,
            control_id=control.id,
            control_nombre=control.nombre,
            fecha_ejecucion=datetime.now(),
            estado=EstadoEjecucion.ERROR,
            mensaje=mensaje,
            parametros_utilizados=parametros,
            resultado_consulta_disparo=resultado_disparo,
            resultados_consultas_disparadas=[],
            tiempo_total_ejecucion_ms=tiempo_total,
            total_filas_disparo=0,
            total_filas_disparadas=0,
            conexion_id=conexion.id,
            conexion_nombre=conexion.nombre
        )