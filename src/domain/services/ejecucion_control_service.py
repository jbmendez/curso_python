"""
Servicio de dominio para la ejecución de controles SQL

Este servicio contiene la lógica de negocio para ejecutar controles
sobre las bases de datos objetivo.
"""
import time
import random
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import jaydebeapi
except ImportError:
    jaydebeapi = None

from src.domain.entities.control import Control
from src.domain.entities.conexion import Conexion
from src.domain.entities.consulta import Consulta
from src.domain.entities.resultado_ejecucion import ResultadoEjecucion, ResultadoConsulta, EstadoEjecucion
from src.domain.repositories.control_repository import ControlRepository
from src.domain.repositories.parametro_repository import ParametroRepository
from src.domain.repositories.consulta_repository import ConsultaRepository
from src.domain.repositories.referente_repository import ReferenteRepository
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository
from src.domain.repositories.conexion_repository import ConexionRepository


class EjecucionControlService:
    """Servicio de dominio para ejecutar controles SQL"""
    
    def __init__(
        self,
        control_repository: ControlRepository,
        parametro_repository: ParametroRepository,
        consulta_repository: ConsultaRepository,
        referente_repository: ReferenteRepository,
        conexion_repository: ConexionRepository,
        consulta_control_repository: ConsultaControlRepository
    ):
        self._control_repository = control_repository
        self._parametro_repository = parametro_repository
        self._consulta_repository = consulta_repository
        self._referente_repository = referente_repository
        self._conexion_repository = conexion_repository
        self._consulta_control_repository = consulta_control_repository
    
    def _es_consulta_lectura(self, sql: str) -> bool:
        """Determina si una consulta SQL es de lectura (devuelve datos)"""
        sql_upper = sql.upper().strip()
        
        # Consultas que devuelven datos
        if sql_upper.startswith('SELECT'):
            return True
        
        # CTE (Common Table Expressions) que terminan en SELECT
        if sql_upper.startswith('WITH') and 'SELECT' in sql_upper:
            return True
        
        # Comandos EXPLAIN, SHOW, DESCRIBE que devuelven datos
        if any(sql_upper.startswith(cmd) for cmd in ['EXPLAIN', 'SHOW', 'DESCRIBE', 'DESC']):
            return True
        
        return False
    
    def _es_procedimiento(self, sql: str) -> bool:
        """Determina si una consulta SQL es un procedimiento almacenado"""
        sql_upper = sql.upper().strip()
        
        # Stored procedures y funciones
        if any(sql_upper.startswith(cmd) for cmd in ['CALL', 'EXECUTE', 'EXEC']):
            return True
        
        return False
    
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
            
            # Obtener asociaciones consulta-control
            asociaciones = self._consulta_control_repository.obtener_por_control(control.id)
            if not asociaciones:
                return self._crear_resultado_error(
                    control, conexion, valores_parametros, 
                    "No se encontraron consultas asociadas al control"
                )
            
            # Buscar consulta de disparo
            asociacion_disparo = next((a for a in asociaciones if a.es_disparo), None)
            if not asociacion_disparo:
                return self._crear_resultado_error(
                    control, conexion, valores_parametros, 
                    "No se encontró consulta de disparo para el control"
                )
            
            # Obtener consulta de disparo
            consulta_disparo = self._consulta_repository.obtener_por_id(asociacion_disparo.consulta_id)
            if not consulta_disparo:
                return self._crear_resultado_error(
                    control, conexion, valores_parametros, 
                    "No se pudo obtener la consulta de disparo"
                )
            
            # Ejecutar consulta de disparo
            resultado_disparo = self._ejecutar_consulta(
                consulta_disparo, valores_parametros, conexion, mock_execution, es_disparo=True
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
            if control_se_dispara and not ejecutar_solo_disparo:
                # Obtener consultas disparadas (no de disparo)
                asociaciones_disparadas = [a for a in asociaciones if not a.es_disparo and a.activa]
                asociaciones_disparadas.sort(key=lambda x: x.orden)  # Ordenar por orden de ejecución
                
                for asociacion in asociaciones_disparadas:
                    consulta = self._consulta_repository.obtener_por_id(asociacion.consulta_id)
                    if consulta:
                        resultado = self._ejecutar_consulta(
                            consulta, valores_parametros, conexion, mock_execution, es_disparo=False
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
        mock_execution: bool = False,
        es_disparo: bool = False
    ) -> ResultadoConsulta:
        """Ejecuta una consulta específica"""
        inicio = time.time()
        
        try:
            if mock_execution:
                # Simular ejecución para demo/testing
                return self._simular_ejecucion_consulta(consulta, parametros, es_disparo)
            else:
                # Ejecución real de la consulta SQL
                return self._ejecutar_consulta_real(consulta, parametros, conexion, es_disparo)
                
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
    
    def _simular_ejecucion_consulta(self, consulta: Consulta, parametros: Dict[str, Any], es_disparo: bool = False) -> ResultadoConsulta:
        """Simula la ejecución de una consulta para demo/testing"""
        sql_ejecutado = self._reemplazar_parametros(consulta.sql, parametros)
        
        # Simular tiempo de ejecución
        tiempo_simulado = random.uniform(10, 100)  # Entre 10ms y 100ms
        
        # Simular resultados según si es consulta de disparo o no
        if es_disparo:
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
    
    def _ejecutar_consulta_real(
        self,
        consulta: Consulta,
        parametros: Dict[str, Any],
        conexion: Conexion,
        es_disparo: bool = False
    ) -> ResultadoConsulta:
        """Ejecuta una consulta real contra la base de datos"""
        inicio = time.time()
        sql_ejecutado = self._reemplazar_parametros(consulta.sql, parametros)
        
        try:
            # Determinar el tipo de conexión y ejecutar
            tipo_motor = conexion.tipo_motor.lower()
            print(f"DEBUG: Ejecutando consulta en motor: {tipo_motor}")
            
            if tipo_motor in ['sqlite', 'sqlite3']:
                return self._ejecutar_sqlite(sql_ejecutado, consulta, inicio)
            elif tipo_motor in ['ibm i series', 'as/400', 'iseries', 'ibm i']:
                return self._ejecutar_ibm_i(sql_ejecutado, conexion, consulta, inicio)
            elif tipo_motor in ['postgresql', 'postgres']:
                return self._ejecutar_postgresql(sql_ejecutado, conexion, consulta, inicio)
            elif tipo_motor in ['sqlserver', 'sql server', 'mssql']:
                return self._ejecutar_sqlserver(sql_ejecutado, conexion, consulta, inicio)
            else:
                # Para tipos no implementados, devolver error en lugar de simulación
                tiempo_ejecucion = (time.time() - inicio) * 1000
                return ResultadoConsulta(
                    consulta_id=consulta.id,
                    consulta_nombre=consulta.nombre,
                    sql_ejecutado=sql_ejecutado,
                    filas_afectadas=0,
                    datos=[],
                    tiempo_ejecucion_ms=tiempo_ejecucion,
                    error=f"Motor de BD no soportado para ejecución real: {conexion.tipo_motor}"
                )
                
        except Exception as e:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql_ejecutado,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=f"Error ejecutando consulta: {str(e)}"
            )
    
    def _ejecutar_sqlite(self, sql: str, consulta: Consulta, inicio: float) -> ResultadoConsulta:
        """Ejecuta consulta en SQLite"""
        try:
            # Para demo, usar una base de datos de ejemplo
            with sqlite3.connect("sistema_controles.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(sql)
                
                if sql.strip().upper().startswith('SELECT'):
                    rows = cursor.fetchall()
                    datos = [dict(row) for row in rows]
                    filas_afectadas = len(datos)
                else:
                    conn.commit()
                    datos = []
                    filas_afectadas = cursor.rowcount
                
                tiempo_ejecucion = (time.time() - inicio) * 1000
                
                return ResultadoConsulta(
                    consulta_id=consulta.id,
                    consulta_nombre=consulta.nombre,
                    sql_ejecutado=sql,
                    filas_afectadas=filas_afectadas,
                    datos=datos,
                    tiempo_ejecucion_ms=tiempo_ejecucion,
                    error=""
                )
                
        except Exception as e:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=f"Error SQLite: {str(e)}"
            )
    
    def _ejecutar_ibm_i(self, sql: str, conexion: Conexion, consulta: Consulta, inicio: float) -> ResultadoConsulta:
        """Ejecuta consulta en IBM i Series usando JDBC"""
        conn = None
        cursor = None
        try:
            # Verificar si jaydebeapi está disponible
            if jaydebeapi is None:
                raise Exception("jaydebeapi no está instalado. Instale con: pip install jaydebeapi")
            
            # Configuración JDBC para IBM i
            driver_path = os.path.join(os.getcwd(), "drivers", "jt400.jar")
            if not os.path.exists(driver_path):
                raise Exception(f"Driver JT400 no encontrado en: {driver_path}")
            
            # Usar puerto por defecto si no se especifica
            puerto = conexion.puerto if conexion.puerto and conexion.puerto > 0 else 446
            
            # Primero, intentar una conexión de prueba simple
            print(f"DEBUG: Verificando conectividad básica...")
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)  # 10 segundos de timeout
                result = sock.connect_ex((conexion.servidor, puerto))
                sock.close()
                if result != 0:
                    raise Exception(f"No se puede conectar al puerto {puerto} en {conexion.servidor}")
                print(f"DEBUG: Puerto {puerto} accesible en {conexion.servidor}")
            except Exception as e:
                raise Exception(f"Error de conectividad de red: {str(e)}")
            
            # Intentar diferentes configuraciones de conexión
            configuraciones = [
                {
                    'url': f"jdbc:as400://{conexion.servidor}:{puerto}",
                    'props': {
                        'user': conexion.usuario,
                        'password': conexion.contraseña or "",
                        'prompt': 'false',
                        'thread used': 'false',
                        'errors': 'full',
                        'naming': 'system',  # Único para IBM i - toma lista de librerías
                        'libraries': '*LIBL',
                        'date format': 'iso',
                        'time format': 'hms'
                    },
                    'descripcion': 'Configuración básica con naming=system'
                },
                {
                    'url': f"jdbc:as400://{conexion.servidor}",
                    'props': {
                        'user': conexion.usuario,
                        'password': conexion.contraseña or "",
                        'prompt': 'false',
                        'secure': 'false',
                        'thread used': 'false',
                        'naming': 'system',  # Único para IBM i - toma lista de librerías
                        'libraries': '*LIBL'
                    },
                    'descripcion': 'Configuración simplificada sin puerto con naming=system'
                },
                {
                    'url': f"jdbc:as400://{conexion.servidor}:{puerto}",
                    'props': {
                        'user': conexion.usuario,
                        'password': conexion.contraseña or "",
                        'prompt': 'false',
                        'secure': 'false',
                        'thread used': 'false',
                        'errors': 'basic',
                        'trace': 'false',
                        'naming': 'system'  # Único para IBM i - toma lista de librerías
                    },
                    'descripcion': 'Configuración sin seguridad con naming=system'
                }
            ]
            
            driver_class = "com.ibm.as400.access.AS400JDBCDriver"
            
            # Probar cada configuración
            for i, config in enumerate(configuraciones):
                print(f"DEBUG: Probando {config['descripcion']} - URL: {config['url']}")
                print(f"DEBUG: Usuario: {conexion.usuario}")
                
                try:
                    # Conectar usando jaydebeapi
                    conn = jaydebeapi.connect(
                        driver_class,
                        config['url'],
                        config['props'],
                        driver_path
                    )
                    
                    print(f"DEBUG: ¡Conexión establecida exitosamente con {config['descripcion']}!")
                    break
                    
                except Exception as e:
                    print(f"DEBUG: Error con {config['descripcion']}: {str(e)}")
                    if i == len(configuraciones) - 1:
                        # Si fue el último intento, lanzar error
                        raise Exception(f"Todos los métodos de conexión fallaron. Último error: {str(e)}")
                    continue
            
            # Si llegamos aquí, la conexión fue exitosa
            # Establecer biblioteca de trabajo si se especifica
            if conexion.base_datos and conexion.base_datos != '*LIBL':
                try:
                    with conn.cursor() as setup_cursor:
                        setup_cursor.execute(f"SET SCHEMA {conexion.base_datos}")
                        print(f"DEBUG: Esquema establecido a: {conexion.base_datos}")
                except Exception as e:
                    print(f"DEBUG: Advertencia - No se pudo establecer esquema: {str(e)}")
            
            cursor = conn.cursor()
            print(f"DEBUG: Ejecutando SQL: {sql}")
            cursor.execute(sql)
            
            if self._es_consulta_lectura(sql):
                # Para consultas de lectura (SELECT, WITH...SELECT, etc.), obtener resultados
                rows = cursor.fetchall()
                # Obtener nombres de columnas
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                
                print(f"DEBUG: Columnas encontradas: {column_names}")
                print(f"DEBUG: Número de filas: {len(rows)}")
                
                # Convertir a lista de diccionarios manejando nombres duplicados
                datos = []
                
                # Crear nombres únicos para columnas duplicadas
                unique_column_names = []
                column_counts = {}
                for col_name in column_names:
                    if col_name in column_counts:
                        column_counts[col_name] += 1
                        unique_name = f"{col_name}_{column_counts[col_name]}"
                    else:
                        column_counts[col_name] = 0
                        unique_name = col_name
                    unique_column_names.append(unique_name)
                
                print(f"DEBUG: Nombres únicos de columnas: {unique_column_names}")
                
                for row in rows:
                    row_dict = {}
                    for i, value in enumerate(row):
                        col_name = unique_column_names[i] if i < len(unique_column_names) else f"col_{i}"
                        # Convertir valores problemáticos
                        if value is None:
                            row_dict[col_name] = None
                        elif isinstance(value, (bytes, bytearray)):
                            # Convertir bytes a string
                            try:
                                row_dict[col_name] = value.decode('utf-8', errors='replace')
                            except:
                                row_dict[col_name] = str(value)
                        else:
                            row_dict[col_name] = str(value) if not isinstance(value, (int, float, bool)) else value
                    datos.append(row_dict)
                
                filas_afectadas = len(datos)
                print(f"DEBUG: Primera fila (si existe): {datos[0] if datos else 'No hay datos'}")
                
            elif self._es_procedimiento(sql):
                # Para stored procedures (CALL, EXECUTE), intentar obtener resultados si los hay
                try:
                    # Algunos procedimientos pueden devolver resultados
                    if cursor.description:
                        rows = cursor.fetchall()
                        column_names = [desc[0] for desc in cursor.description]
                        
                        # Crear nombres únicos para columnas duplicadas
                        unique_column_names = []
                        column_counts = {}
                        for col_name in column_names:
                            if col_name in column_counts:
                                column_counts[col_name] += 1
                                unique_name = f"{col_name}_{column_counts[col_name]}"
                            else:
                                column_counts[col_name] = 0
                                unique_name = col_name
                            unique_column_names.append(unique_name)
                        
                        datos = []
                        for row in rows:
                            row_dict = {}
                            for i, value in enumerate(row):
                                col_name = unique_column_names[i] if i < len(unique_column_names) else f"col_{i}"
                                if value is None:
                                    row_dict[col_name] = None
                                elif isinstance(value, (bytes, bytearray)):
                                    try:
                                        row_dict[col_name] = value.decode('utf-8', errors='replace')
                                    except:
                                        row_dict[col_name] = str(value)
                                else:
                                    row_dict[col_name] = str(value) if not isinstance(value, (int, float, bool)) else value
                            datos.append(row_dict)
                        
                        filas_afectadas = len(datos)
                        print(f"DEBUG: Procedimiento devolvió {filas_afectadas} filas")
                        print(f"DEBUG: Columnas del procedimiento: {unique_column_names}")
                    else:
                        # Procedimiento sin resultados
                        datos = []
                        filas_afectadas = 1  # Indicar que se ejecutó exitosamente
                        print(f"DEBUG: Procedimiento ejecutado exitosamente sin resultados")
                except Exception as e:
                    print(f"DEBUG: Error procesando resultados del procedimiento: {str(e)}")
                    datos = []
                    filas_afectadas = 1  # Asumir que se ejecutó si no hay error mayor
            else:
                # Para INSERT/UPDATE/DELETE y otros comandos
                conn.commit()
                datos = []
                filas_afectadas = cursor.rowcount
                print(f"DEBUG: Filas afectadas: {filas_afectadas}")
            
            tiempo_ejecucion = (time.time() - inicio) * 1000
            
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=filas_afectadas,
                datos=datos,
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=""
            )
            
        except Exception as e:
            error_msg = str(e)
            print(f"DEBUG: Error en IBM i: {error_msg}")
            
            # Información adicional para debugging
            if "connection" in error_msg.lower():
                print("DEBUG: Sugerencias detalladas para error de conexión:")
                print("1. Verificar que el servidor IBM i esté accesible con ping")
                print("2. Verificar credenciales de usuario y que no esté bloqueado")
                print("3. Verificar que el puerto 446 esté abierto en firewall")
                print("4. Verificar que el servicio QZDASOINIT esté ejecutándose")
                print("5. Verificar si hay restricciones de IP en IBM i")
                print("6. Probar con telnet: telnet 172.20.0.10 446")
                print(f"7. Verificar configuración de servidor: QZDASOINIT job status")
            
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=f"Error IBM i: {error_msg}"
            )
        finally:
            # Asegurar cierre de recursos
            try:
                if cursor:
                    cursor.close()
                    print("DEBUG: Cursor cerrado")
                if conn:
                    conn.close()
                    print("DEBUG: Conexión cerrada")
            except Exception as e:
                print(f"DEBUG: Error cerrando recursos: {str(e)}")
    
    def _ejecutar_postgresql(self, sql: str, conexion: Conexion, consulta: Consulta, inicio: float) -> ResultadoConsulta:
        """Ejecuta consulta en PostgreSQL"""
        try:
            import psycopg2
            import psycopg2.extras
            
            # Construir cadena de conexión
            conn_string = f"host={conexion.servidor} port={conexion.puerto or 5432} dbname={conexion.base_datos} user={conexion.usuario}"
            if conexion.contraseña:
                conn_string += f" password={conexion.contraseña}"
            
            print(f"DEBUG: Conectando a PostgreSQL: {conn_string}")
            
            with psycopg2.connect(conn_string) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    print(f"DEBUG: Ejecutando SQL: {sql}")
                    cursor.execute(sql)
                    
                    if self._es_consulta_lectura(sql):
                        rows = cursor.fetchall()
                        datos = [dict(row) for row in rows]
                        filas_afectadas = len(datos)
                        print(f"DEBUG: Columnas encontradas: {list(datos[0].keys()) if datos else []}")
                        print(f"DEBUG: Número de filas: {len(datos)}")
                        print(f"DEBUG: Primera fila (si existe): {datos[0] if datos else 'No hay datos'}")
                    else:
                        conn.commit()
                        datos = []
                        filas_afectadas = cursor.rowcount
                        print(f"DEBUG: Filas afectadas: {filas_afectadas}")
                    
                    tiempo_ejecucion = (time.time() - inicio) * 1000
                    
                    return ResultadoConsulta(
                        consulta_id=consulta.id,
                        consulta_nombre=consulta.nombre,
                        sql_ejecutado=sql,
                        filas_afectadas=filas_afectadas,
                        datos=datos,
                        tiempo_ejecucion_ms=tiempo_ejecucion,
                        error=""
                    )
                    
        except ImportError:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error="psycopg2 no está instalado. Instale con: pip install psycopg2"
            )
        except Exception as e:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=f"Error PostgreSQL: {str(e)}"
            )
    
    def _ejecutar_sqlserver(self, sql: str, conexion: Conexion, consulta: Consulta, inicio: float) -> ResultadoConsulta:
        """Ejecuta consulta en SQL Server"""
        try:
            import pyodbc
            
            # Construir cadena de conexión
            conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexion.servidor},{conexion.puerto or 1433};DATABASE={conexion.base_datos};UID={conexion.usuario}"
            if conexion.contraseña:
                conn_string += f";PWD={conexion.contraseña}"
            else:
                conn_string += ";Trusted_Connection=yes"
            
            print(f"DEBUG: Conectando a SQL Server: {conn_string}")
            
            with pyodbc.connect(conn_string) as conn:
                cursor = conn.cursor()
                print(f"DEBUG: Ejecutando SQL: {sql}")
                cursor.execute(sql)
                
                if self._es_consulta_lectura(sql):
                    # Para consultas de lectura (SELECT, WITH...SELECT, etc.), obtener resultados
                    # Obtener nombres de columnas
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()
                    
                    print(f"DEBUG: Columnas encontradas: {columns}")
                    print(f"DEBUG: Número de filas: {len(rows)}")
                    
                    # Convertir a lista de diccionarios manejando nombres duplicados
                    datos = []
                    
                    # Crear nombres únicos para columnas duplicadas
                    unique_column_names = []
                    column_counts = {}
                    for col_name in columns:
                        if col_name in column_counts:
                            column_counts[col_name] += 1
                            unique_name = f"{col_name}_{column_counts[col_name]}"
                        else:
                            column_counts[col_name] = 0
                            unique_name = col_name
                        unique_column_names.append(unique_name)
                    
                    print(f"DEBUG: Nombres únicos de columnas: {unique_column_names}")
                    
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            col_name = unique_column_names[i] if i < len(unique_column_names) else f"col_{i}"
                            # Convertir valores problemáticos
                            if value is None:
                                row_dict[col_name] = None
                            else:
                                row_dict[col_name] = str(value) if not isinstance(value, (int, float, bool)) else value
                        datos.append(row_dict)
                    
                    filas_afectadas = len(datos)
                    print(f"DEBUG: Primera fila (si existe): {datos[0] if datos else 'No hay datos'}")
                else:
                    conn.commit()
                    datos = []
                    filas_afectadas = cursor.rowcount
                    print(f"DEBUG: Filas afectadas: {filas_afectadas}")
                
                tiempo_ejecucion = (time.time() - inicio) * 1000
                
                return ResultadoConsulta(
                    consulta_id=consulta.id,
                    consulta_nombre=consulta.nombre,
                    sql_ejecutado=sql,
                    filas_afectadas=filas_afectadas,
                    datos=datos,
                    tiempo_ejecucion_ms=tiempo_ejecucion,
                    error=""
                )
                
        except ImportError:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error="pyodbc no está instalado. Instale con: pip install pyodbc"
            )
        except Exception as e:
            tiempo_ejecucion = (time.time() - inicio) * 1000
            return ResultadoConsulta(
                consulta_id=consulta.id,
                consulta_nombre=consulta.nombre,
                sql_ejecutado=sql,
                filas_afectadas=0,
                datos=[],
                tiempo_ejecucion_ms=tiempo_ejecucion,
                error=f"Error SQL Server: {str(e)}"
            )