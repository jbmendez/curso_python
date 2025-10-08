"""
Motor de Ejecución Automática de Controles
==========================================

Este módulo implementa un motor básico que ejecuta controles
según su programación automática definida.

Características:
- Loop continuo cada 1 minuto
- Ejecución secuencial de controles
- Logging detallado
- Gestión de errores
- Fácil de extender
"""
import time
import logging
import signal
import sys
from datetime import datetime
from typing import List, Optional
from pathlib import Path

# Agregar src al path para imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.infrastructure.database.database_setup import DatabaseSetup
from src.infrastructure.repositories.sqlite_programacion_repository import SQLiteProgramacionRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.application.use_cases.listar_programaciones_use_case import ListarProgramacionesUseCase
from src.domain.services.ejecucion_control_service import EjecucionControlService
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.infrastructure.repositories.sqlite_consulta_control_repository import SQLiteConsultaControlRepository
from src.infrastructure.repositories.sqlite_control_referente_repository import SQLiteControlReferenteRepository


class MotorEjecucionService:
    """
    Motor de ejecución automática de controles programados
    """
    
    def __init__(self):
        self.ejecutando = False
        self.intervalo_segundos = 60  # 1 minuto
        self.setup_logging()
        self.setup_dependencies()
        self.setup_signal_handlers()
        
    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                # Archivo de log rotativo
                logging.FileHandler(
                    log_dir / f"motor_ejecucion_{datetime.now().strftime('%Y%m%d')}.log",
                    encoding='utf-8'
                ),
                # Consola
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("MotorEjecucion")
        self.logger.info("🚀 Motor de Ejecución iniciado")
        
    def setup_dependencies(self):
        """Configura las dependencias e inyección"""
        try:
            # Configurar base de datos
            db_path = "sistema_controles.db"
            db_setup = DatabaseSetup(db_path)
            db_setup.initialize_database()
            
            # Repositorios
            self.programacion_repo = SQLiteProgramacionRepository(db_path)
            self.control_repo = SQLiteControlRepository(db_path)
            self.conexion_repo = SQLiteConexionRepository(db_path)
            self.parametro_repo = SQLiteParametroRepository(db_path)
            self.consulta_repo = SQLiteConsultaRepository(db_path)
            self.referente_repo = SQLiteReferenteRepository(db_path)
            self.consulta_control_repo = SQLiteConsultaControlRepository(db_path)
            self.control_referente_repo = SQLiteControlReferenteRepository(db_path)
            
            # Use cases
            self.listar_programaciones_uc = ListarProgramacionesUseCase(
                self.programacion_repo, 
                self.control_repo
            )
            
            # Servicios
            self.ejecucion_service = EjecucionControlService(
                self.control_repo,
                self.parametro_repo,
                self.consulta_repo,
                self.referente_repo,
                self.conexion_repo,
                self.consulta_control_repo,
                self.control_referente_repo
            )
            
            self.logger.info("✅ Dependencias configuradas correctamente")
            
        except Exception as e:
            self.logger.error(f"❌ Error configurando dependencias: {e}")
            raise
    
    def setup_signal_handlers(self):
        """Configura manejadores de señales para parada elegante"""
        def signal_handler(signum, frame):
            self.logger.info(f"📡 Señal recibida: {signum}")
            self.detener()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def iniciar(self):
        """Inicia el motor de ejecución"""
        self.logger.info("🔄 Iniciando motor de ejecución automática")
        
        # Crear archivo PID
        self._crear_archivo_pid()
        
        self.ejecutando = True
        
        try:
            while self.ejecutando:
                inicio_ciclo = time.time()
                
                try:
                    self.ejecutar_ciclo()
                except Exception as e:
                    self.logger.error(f"❌ Error en ciclo de ejecución: {e}")
                
                # Calcular tiempo de espera para mantener intervalo
                tiempo_transcurrido = time.time() - inicio_ciclo
                tiempo_espera = max(0, self.intervalo_segundos - tiempo_transcurrido)
                
                if tiempo_espera > 0:
                    self.logger.debug(f"⏳ Esperando {tiempo_espera:.1f}s hasta próximo ciclo")
                    time.sleep(tiempo_espera)
                else:
                    self.logger.warning(f"⚠️ Ciclo tardó {tiempo_transcurrido:.1f}s (más de {self.intervalo_segundos}s)")
                
        except KeyboardInterrupt:
            self.logger.info("⌨️ Interrupción de teclado recibida")
        except Exception as e:
            self.logger.error(f"💥 Error fatal en motor: {e}")
        finally:
            self.detener()
    
    def _crear_archivo_pid(self):
        """Crea archivo con PID del proceso"""
        try:
            import os
            with open("motor.pid", "w") as f:
                f.write(str(os.getpid()))
            self.logger.debug(f"📄 Archivo PID creado: {os.getpid()}")
        except Exception as e:
            self.logger.warning(f"⚠️ No se pudo crear archivo PID: {e}")
    
    def _eliminar_archivo_pid(self):
        """Elimina archivo PID"""
        try:
            pid_file = Path("motor.pid")
            if pid_file.exists():
                pid_file.unlink()
                self.logger.debug("📄 Archivo PID eliminado")
        except Exception as e:
            self.logger.warning(f"⚠️ No se pudo eliminar archivo PID: {e}")
    
    def ejecutar_ciclo(self):
        """Ejecuta un ciclo completo de verificación y ejecución"""
        ciclo_inicio = datetime.now()
        self.logger.debug(f"🔍 Iniciando ciclo: {ciclo_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Obtener programaciones pendientes
        programaciones_pendientes = self.obtener_programaciones_pendientes()
        
        if not programaciones_pendientes:
            self.logger.debug("😴 No hay programaciones pendientes")
            return
        
        self.logger.info(f"📋 Encontradas {len(programaciones_pendientes)} programaciones pendientes")
        
        # Ejecutar cada programación (secuencial)
        for programacion in programaciones_pendientes:
            try:
                self.ejecutar_programacion(programacion)
            except Exception as e:
                self.logger.error(f"❌ Error ejecutando programación {programacion.nombre}: {e}")
        
        ciclo_fin = datetime.now()
        duracion = (ciclo_fin - ciclo_inicio).total_seconds()
        self.logger.debug(f"✅ Ciclo completado en {duracion:.2f}s")
    
    def obtener_programaciones_pendientes(self) -> List:
        """Obtiene programaciones que deben ejecutarse ahora"""
        try:
            # Obtener programaciones activas directamente del repositorio
            programaciones = self.programacion_repo.obtener_activas()
            
            # Filtrar las que deben ejecutarse ahora
            pendientes = []
            ahora = datetime.now()
            
            for programacion in programaciones:
                try:
                    if programacion.debe_ejecutarse_ahora(ahora):
                        pendientes.append(programacion)
                        self.logger.debug(f"⏰ Programación pendiente: {programacion.nombre}")
                except Exception as e:
                    self.logger.error(f"❌ Error evaluando programación {programacion.nombre}: {e}")
            
            return pendientes
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo programaciones pendientes: {e}")
            return []
    
    def ejecutar_programacion(self, programacion):
        """Ejecuta una programación específica"""
        inicio = time.time()
        self.logger.info(f"🚀 Ejecutando programación: {programacion.nombre} (Control ID: {programacion.control_id})")
        
        try:
            # Obtener control
            control = self.control_repo.obtener_por_id(programacion.control_id)
            if not control:
                raise Exception(f"Control {programacion.control_id} no encontrado")
            
            # Obtener conexión del control
            conexion = self.conexion_repo.obtener_por_id(control.conexion_id) if control.conexion_id else None
            if not conexion:
                raise Exception(f"Conexión {control.conexion_id} no encontrada para control {control.nombre}")
            
            # Ejecutar control
            resultado = self.ejecucion_service.ejecutar_control(
                control=control,
                conexion=conexion,
                parametros_adicionales={},
                ejecutar_solo_disparo=False,
                mock_execution=False  # Cambiar a True para testing
            )
            
            # Marcar programación como ejecutada
            programacion.marcar_ejecutado()
            
            # Recalcular próxima ejecución
            programacion._calcular_proxima_ejecucion()
            
            # Actualizar en base de datos
            self.programacion_repo.actualizar(programacion)
            
            # Log del resultado
            duracion = time.time() - inicio
            self.logger.info(
                f"✅ Programación {programacion.nombre} ejecutada exitosamente "
                f"({duracion:.2f}s) - Estado: {resultado.estado.value}"
            )
            
            if resultado.mensaje:
                self.logger.info(f"📄 Mensaje: {resultado.mensaje}")
            
        except Exception as e:
            duracion = time.time() - inicio
            self.logger.error(
                f"❌ Error ejecutando programación {programacion.nombre} "
                f"({duracion:.2f}s): {e}"
            )
    
    def detener(self):
        """Detiene el motor de ejecución"""
        if self.ejecutando:
            self.logger.info("🛑 Deteniendo motor de ejecución...")
            self.ejecutando = False
            self._eliminar_archivo_pid()
        else:
            self.logger.info("🛑 Motor ya estaba detenido")
    
    def estado(self) -> dict:
        """Obtiene el estado actual del motor"""
        return {
            'ejecutando': self.ejecutando,
            'intervalo_segundos': self.intervalo_segundos,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Función principal para ejecutar el motor"""
    print("🏭 Motor de Ejecución Automática de Controles")
    print("=" * 50)
    
    motor = MotorEjecucionService()
    
    try:
        motor.iniciar()
    except Exception as e:
        print(f"💥 Error fatal: {e}")
        sys.exit(1)
    
    print("👋 Motor detenido")


if __name__ == "__main__":
    main()