"""
Monitor de Archivos de Notificación
Script que monitorea carpetas compartidas en busca de archivos de notificación,
los procesa mostrando notificaciones locales y luego los elimina.
"""

import os
import time
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Importar servicios
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.services.notification_service import WindowsNotificationService
from src.infrastructure.services.notification_file_service import NotificationFileService


class NotificationFileMonitor:
    """Monitor de archivos de notificación en carpetas compartidas"""
    
    def __init__(self, carpetas_monitoreadas: List[str], intervalo_segundos: int = 5):
        """
        Inicializa el monitor de archivos
        
        Args:
            carpetas_monitoreadas: Lista de carpetas a monitorear
            intervalo_segundos: Intervalo entre verificaciones
        """
        self.carpetas_monitoreadas = carpetas_monitoreadas
        self.intervalo_segundos = intervalo_segundos
        self.notification_service = WindowsNotificationService()
        self.file_service = NotificationFileService()
        self.archivos_procesados = set()  # Para evitar procesar el mismo archivo múltiples veces
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        self._configurar_logging()
        
        self.logger.info(f"Monitor inicializado para {len(carpetas_monitoreadas)} carpetas")
        self.logger.info(f"Intervalo de monitoreo: {intervalo_segundos} segundos")
    
    def _configurar_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitor_notificaciones.log'),
                logging.StreamHandler()
            ]
        )
    
    def iniciar_monitoreo(self):
        """Inicia el monitoreo continuo de las carpetas"""
        self.logger.info("=== INICIANDO MONITOR DE NOTIFICACIONES ===")
        self.logger.info(f"Carpetas monitoreadas:")
        for carpeta in self.carpetas_monitoreadas:
            self.logger.info(f"  - {carpeta}")
        
        # Mostrar notificación de inicio del monitor
        self.notification_service.mostrar_motor_iniciado()
        
        try:
            while True:
                self._procesar_ciclo_monitoreo()
                time.sleep(self.intervalo_segundos)
                
        except KeyboardInterrupt:
            self.logger.info("Monitor detenido por el usuario (Ctrl+C)")
            self.notification_service.mostrar_motor_detenido()
        except Exception as e:
            self.logger.error(f"Error en el monitor: {e}")
            self.notification_service.mostrar_motor_parado(f"Error en monitor: {str(e)}")
    
    def _procesar_ciclo_monitoreo(self):
        """Procesa un ciclo de monitoreo de todas las carpetas"""
        archivos_encontrados = 0
        archivos_procesados = 0
        
        for carpeta in self.carpetas_monitoreadas:
            if not os.path.exists(carpeta):
                continue
            
            # Obtener archivos de notificación
            archivos = self.file_service.listar_archivos_notificacion(carpeta)
            archivos_encontrados += len(archivos)
            
            for archivo in archivos:
                # Evitar procesar el mismo archivo múltiples veces
                if archivo in self.archivos_procesados:
                    continue
                
                if self._procesar_archivo_notificacion(archivo):
                    archivos_procesados += 1
                    self.archivos_procesados.add(archivo)
        
        # Log periódico solo si hay actividad
        if archivos_encontrados > 0:
            self.logger.info(f"Ciclo completado: {archivos_procesados}/{archivos_encontrados} archivos procesados")
    
    def _procesar_archivo_notificacion(self, ruta_archivo: str) -> bool:
        """
        Procesa un archivo de notificación específico
        
        Args:
            ruta_archivo: Ruta del archivo a procesar
            
        Returns:
            bool: True si se procesó exitosamente
        """
        try:
            self.logger.info(f"Procesando archivo: {os.path.basename(ruta_archivo)}")
            
            # Leer archivo de notificación
            datos = self.file_service.leer_archivo_notificacion(ruta_archivo)
            if not datos:
                self.logger.error(f"No se pudo leer archivo: {ruta_archivo}")
                return False
            
            # Procesar según tipo de notificación
            exito = self._mostrar_notificacion_segun_tipo(datos)
            
            if exito:
                # Eliminar archivo después de procesarlo exitosamente
                if self.file_service.eliminar_archivo_notificacion(ruta_archivo):
                    self.logger.info(f"Archivo procesado y eliminado: {os.path.basename(ruta_archivo)}")
                    return True
                else:
                    self.logger.warning(f"Archivo procesado pero no se pudo eliminar: {ruta_archivo}")
                    return False
            else:
                self.logger.error(f"Error al mostrar notificación para archivo: {ruta_archivo}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error procesando archivo {ruta_archivo}: {e}")
            return False
    
    def _mostrar_notificacion_segun_tipo(self, datos: Dict[str, Any]) -> bool:
        """
        Muestra notificación según el tipo de evento
        
        Args:
            datos: Datos del archivo de notificación
            
        Returns:
            bool: True si se mostró exitosamente
        """
        tipo = datos.get('tipo', 'unknown')
        
        try:
            if tipo == 'control_disparado':
                return self._mostrar_notificacion_control_disparado(datos)
            elif tipo == 'control_error':
                return self._mostrar_notificacion_control_error(datos)
            elif tipo in ['motor_iniciado', 'motor_detenido', 'motor_parado']:
                return self._mostrar_notificacion_motor(datos)
            else:
                self.logger.warning(f"Tipo de notificación desconocido: {tipo}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error mostrando notificación tipo {tipo}: {e}")
            return False
    
    def _mostrar_notificacion_control_disparado(self, datos: Dict[str, Any]) -> bool:
        """Muestra notificación de control disparado"""
        control_info = datos.get('control', {})
        mensaje_info = datos.get('mensaje', {})
        sistema_info = datos.get('sistema', {})
        
        control_nombre = control_info.get('nombre', 'Control desconocido')
        filas_procesadas = control_info.get('filas_procesadas', 0)
        tiempo_ejecucion_ms = control_info.get('tiempo_ejecucion_ms', 0)
        
        # Agregar información del equipo origen
        equipo_origen = sistema_info.get('equipo_origen', 'Desconocido')
        mensaje_adicional = f"Origen: {equipo_origen}"
        
        return self.notification_service.mostrar_control_disparado(
            control_nombre=control_nombre,
            filas_procesadas=filas_procesadas,
            tiempo_ejecucion_ms=tiempo_ejecucion_ms,
            mensaje_adicional=mensaje_adicional
        )
    
    def _mostrar_notificacion_control_error(self, datos: Dict[str, Any]) -> bool:
        """Muestra notificación de error en control"""
        control_info = datos.get('control', {})
        error_info = datos.get('error', {})
        sistema_info = datos.get('sistema', {})
        
        control_nombre = control_info.get('nombre', 'Control desconocido')
        error_mensaje = error_info.get('mensaje_corto', error_info.get('mensaje', 'Error desconocido'))
        tiempo_ejecucion_ms = control_info.get('tiempo_ejecucion_ms')
        
        # Agregar información del equipo origen
        equipo_origen = sistema_info.get('equipo_origen', 'Desconocido')
        error_completo = f"{error_mensaje}\n\nOrigen: {equipo_origen}"
        
        return self.notification_service.mostrar_control_error(
            control_nombre=control_nombre,
            error_mensaje=error_completo,
            tiempo_ejecucion_ms=tiempo_ejecucion_ms
        )
    
    def _mostrar_notificacion_motor(self, datos: Dict[str, Any]) -> bool:
        """Muestra notificación de evento del motor"""
        tipo = datos.get('tipo', '')
        motor_info = datos.get('motor', {})
        sistema_info = datos.get('sistema', {})
        
        equipo_origen = sistema_info.get('equipo_origen', 'Desconocido')
        
        if tipo == 'motor_iniciado':
            mensaje = f"Motor iniciado en: {equipo_origen}"
            return self.notification_service._mostrar_notificacion(
                "🚀 Motor Remoto Iniciado", mensaje, timeout=8
            )
        elif tipo == 'motor_detenido':
            mensaje = f"Motor detenido en: {equipo_origen}"
            return self.notification_service._mostrar_notificacion(
                "⏹️ Motor Remoto Detenido", mensaje, timeout=5
            )
        elif tipo == 'motor_parado':
            razon = motor_info.get('razon', 'Razón desconocida')
            mensaje = f"Motor parado en: {equipo_origen}\nRazón: {razon}"
            return self.notification_service._mostrar_notificacion(
                "🛑 Motor Remoto Parado", mensaje, timeout=10
            )
        
        return False
    
    def verificar_carpetas(self) -> bool:
        """
        Verifica que las carpetas monitoreadas existan y sean accesibles
        
        Returns:
            bool: True si todas las carpetas son válidas
        """
        carpetas_validas = 0
        
        for carpeta in self.carpetas_monitoreadas:
            if os.path.exists(carpeta) and os.access(carpeta, os.R_OK):
                self.logger.info(f"Carpeta válida: {carpeta}")
                carpetas_validas += 1
            else:
                self.logger.warning(f"Carpeta no accesible: {carpeta}")
        
        exito = carpetas_validas == len(self.carpetas_monitoreadas)
        
        if exito:
            self.logger.info(f"Todas las {carpetas_validas} carpetas son válidas")
        else:
            self.logger.warning(f"Solo {carpetas_validas}/{len(self.carpetas_monitoreadas)} carpetas son válidas")
        
        return exito
    
    def procesar_archivo_unico(self, ruta_archivo: str) -> bool:
        """
        Procesa un archivo de notificación específico (para testing)
        
        Args:
            ruta_archivo: Ruta del archivo a procesar
            
        Returns:
            bool: True si se procesó exitosamente
        """
        self.logger.info(f"Procesando archivo único: {ruta_archivo}")
        return self._procesar_archivo_notificacion(ruta_archivo)


def cargar_configuracion_carpetas(archivo_config: str = None) -> List[str]:
    """
    Carga la configuración de carpetas desde un archivo JSON
    
    Args:
        archivo_config: Ruta del archivo de configuración
        
    Returns:
        list: Lista de carpetas a monitorear
    """
    if archivo_config and os.path.exists(archivo_config):
        try:
            with open(archivo_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('carpetas_monitoreadas', [])
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    # Configuración por defecto
    return [
        r"C:\temp\reportes_test",  # Carpeta de pruebas local
        # r"\\servidor\reportes",    # Ejemplo de carpeta de red
        # r"Z:\notificaciones",      # Ejemplo de unidad mapeada
    ]


def main():
    """Función principal del monitor"""
    parser = argparse.ArgumentParser(description='Monitor de Archivos de Notificación')
    parser.add_argument('--config', '-c', help='Archivo de configuración JSON')
    parser.add_argument('--intervalo', '-i', type=int, default=5, help='Intervalo en segundos (default: 5)')
    parser.add_argument('--test-archivo', '-t', help='Procesar un archivo específico (modo test)')
    parser.add_argument('--verificar-carpetas', '-v', action='store_true', help='Solo verificar carpetas y salir')
    
    args = parser.parse_args()
    
    # Cargar configuración
    carpetas = cargar_configuracion_carpetas(args.config)
    
    if not carpetas:
        print("❌ No hay carpetas configuradas para monitorear")
        print("Edita la configuración o usa --config para especificar un archivo")
        return 1
    
    # Crear monitor
    monitor = NotificationFileMonitor(carpetas, args.intervalo)
    
    # Modo verificación de carpetas
    if args.verificar_carpetas:
        exito = monitor.verificar_carpetas()
        return 0 if exito else 1
    
    # Modo test de archivo único
    if args.test_archivo:
        if os.path.exists(args.test_archivo):
            exito = monitor.procesar_archivo_unico(args.test_archivo)
            print(f"Resultado: {'✅ Éxito' if exito else '❌ Error'}")
            return 0 if exito else 1
        else:
            print(f"❌ Archivo no encontrado: {args.test_archivo}")
            return 1
    
    # Verificar carpetas antes de iniciar monitoreo
    if not monitor.verificar_carpetas():
        print("⚠️ Algunas carpetas no son accesibles. ¿Continuar? (y/N)")
        if input().lower() != 'y':
            return 1
    
    # Iniciar monitoreo continuo
    monitor.iniciar_monitoreo()
    return 0


if __name__ == "__main__":
    exit(main())