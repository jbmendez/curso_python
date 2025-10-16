"""
Servicio para generar archivos de notificación
Se depositan en carpeta compartida junto con Excel para que otros equipos los procesen
"""

import json
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class NotificationFileService:
    """Servicio para crear archivos de notificación en carpeta compartida"""
    
    def __init__(self):
        """Inicializa el servicio de archivos de notificación"""
        self.logger = logging.getLogger(__name__)
    
    def crear_archivo_notificacion_control(
        self,
        carpeta_destino: str,
        control_nombre: str,
        filas_procesadas: int,
        tiempo_ejecucion_ms: float,
        archivo_excel: str = None,
        mensaje_adicional: str = None
    ) -> str:
        """
        Crea un archivo de notificación cuando un control se dispara
        
        Args:
            carpeta_destino: Ruta donde crear el archivo
            control_nombre: Nombre del control disparado
            filas_procesadas: Número de filas procesadas
            tiempo_ejecucion_ms: Tiempo de ejecución en milisegundos
            archivo_excel: Nombre del archivo Excel generado (opcional)
            mensaje_adicional: Mensaje adicional (opcional)
            
        Returns:
            str: Ruta del archivo de notificación creado
        """
        try:
            # Crear timestamp único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # milliseconds
            nombre_archivo = f"notif_control_{timestamp}.json"
            ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
            
            # Preparar datos de notificación
            datos_notificacion = {
                "tipo": "control_disparado",
                "timestamp": datetime.now().isoformat(),
                "control": {
                    "nombre": control_nombre,
                    "filas_procesadas": filas_procesadas,
                    "tiempo_ejecucion_ms": tiempo_ejecucion_ms
                },
                "archivos": {
                    "excel": archivo_excel
                },
                "mensaje": {
                    "titulo": f"🔥 Control Disparado: {control_nombre}",
                    "cuerpo": self._generar_mensaje_control(control_nombre, filas_procesadas, tiempo_ejecucion_ms, mensaje_adicional)
                },
                "sistema": {
                    "equipo_origen": os.getenv('COMPUTERNAME', 'Unknown'),
                    "usuario_origen": os.getenv('USERNAME', 'Unknown')
                }
            }
            
            # Crear directorio si no existe
            os.makedirs(carpeta_destino, exist_ok=True)
            
            # Escribir archivo JSON
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_notificacion, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Archivo de notificación creado: {ruta_archivo}")
            return ruta_archivo
            
        except Exception as e:
            self.logger.error(f"Error al crear archivo de notificación: {e}")
            return None
    
    def crear_archivo_notificacion_error(
        self,
        carpeta_destino: str,
        control_nombre: str,
        error_mensaje: str,
        tiempo_ejecucion_ms: float = None
    ) -> str:
        """
        Crea un archivo de notificación cuando un control falla
        
        Args:
            carpeta_destino: Ruta donde crear el archivo
            control_nombre: Nombre del control que falló
            error_mensaje: Mensaje de error
            tiempo_ejecucion_ms: Tiempo de ejecución en milisegundos (opcional)
            
        Returns:
            str: Ruta del archivo de notificación creado
        """
        try:
            # Crear timestamp único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            nombre_archivo = f"notif_error_{timestamp}.json"
            ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
            
            # Preparar datos de notificación
            datos_notificacion = {
                "tipo": "control_error",
                "timestamp": datetime.now().isoformat(),
                "control": {
                    "nombre": control_nombre,
                    "tiempo_ejecucion_ms": tiempo_ejecucion_ms
                },
                "error": {
                    "mensaje": error_mensaje,
                    "mensaje_corto": error_mensaje[:100] + "..." if len(error_mensaje) > 100 else error_mensaje
                },
                "mensaje": {
                    "titulo": f"❌ Error en Control: {control_nombre}",
                    "cuerpo": self._generar_mensaje_error(control_nombre, error_mensaje, tiempo_ejecucion_ms)
                },
                "sistema": {
                    "equipo_origen": os.getenv('COMPUTERNAME', 'Unknown'),
                    "usuario_origen": os.getenv('USERNAME', 'Unknown')
                }
            }
            
            # Crear directorio si no existe
            os.makedirs(carpeta_destino, exist_ok=True)
            
            # Escribir archivo JSON
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_notificacion, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Archivo de notificación de error creado: {ruta_archivo}")
            return ruta_archivo
            
        except Exception as e:
            self.logger.error(f"Error al crear archivo de notificación de error: {e}")
            return None
    
    def crear_archivo_notificacion_motor(
        self,
        carpeta_destino: str,
        tipo_evento: str,  # "iniciado", "detenido", "parado"
        razon: str = None
    ) -> str:
        """
        Crea un archivo de notificación para eventos del motor
        
        Args:
            carpeta_destino: Ruta donde crear el archivo
            tipo_evento: Tipo de evento del motor
            razon: Razón del evento (opcional)
            
        Returns:
            str: Ruta del archivo de notificación creado
        """
        try:
            # Crear timestamp único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            nombre_archivo = f"notif_motor_{timestamp}.json"
            ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
            
            # Mapear iconos y títulos
            mapeo_eventos = {
                "iniciado": ("🚀", "Motor de Controles Iniciado"),
                "detenido": ("⏹️", "Motor de Controles Detenido"),
                "parado": ("🛑", "Motor de Controles Parado")
            }
            
            icono, titulo_base = mapeo_eventos.get(tipo_evento, ("ℹ️", f"Motor - {tipo_evento}"))
            
            # Preparar datos de notificación
            datos_notificacion = {
                "tipo": f"motor_{tipo_evento}",
                "timestamp": datetime.now().isoformat(),
                "motor": {
                    "evento": tipo_evento,
                    "razon": razon
                },
                "mensaje": {
                    "titulo": f"{icono} {titulo_base}",
                    "cuerpo": self._generar_mensaje_motor(tipo_evento, razon)
                },
                "sistema": {
                    "equipo_origen": os.getenv('COMPUTERNAME', 'Unknown'),
                    "usuario_origen": os.getenv('USERNAME', 'Unknown')
                }
            }
            
            # Crear directorio si no existe
            os.makedirs(carpeta_destino, exist_ok=True)
            
            # Escribir archivo JSON
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_notificacion, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Archivo de notificación de motor creado: {ruta_archivo}")
            return ruta_archivo
            
        except Exception as e:
            self.logger.error(f"Error al crear archivo de notificación de motor: {e}")
            return None
    
    def _generar_mensaje_control(
        self, 
        control_nombre: str, 
        filas_procesadas: int, 
        tiempo_ejecucion_ms: float, 
        mensaje_adicional: str = None
    ) -> str:
        """Genera el mensaje para notificación de control disparado"""
        tiempo_str = f"{tiempo_ejecucion_ms:.0f}ms" if tiempo_ejecucion_ms < 1000 else f"{tiempo_ejecucion_ms/1000:.1f}s"
        
        mensaje = f"Se ha disparado el control: {control_nombre}\n"
        mensaje += f"Filas procesadas: {filas_procesadas}\n"
        mensaje += f"Tiempo de ejecución: {tiempo_str}"
        
        if mensaje_adicional:
            mensaje += f"\n\nDetalles: {mensaje_adicional}"
        
        return mensaje
    
    def _generar_mensaje_error(
        self, 
        control_nombre: str, 
        error_mensaje: str, 
        tiempo_ejecucion_ms: float = None
    ) -> str:
        """Genera el mensaje para notificación de error"""
        mensaje = f"Error en control: {control_nombre}\n"
        
        # Limitar longitud del mensaje de error para notificación
        error_corto = error_mensaje[:200] + "..." if len(error_mensaje) > 200 else error_mensaje
        mensaje += f"Error: {error_corto}"
        
        if tiempo_ejecucion_ms:
            tiempo_str = f"{tiempo_ejecucion_ms:.0f}ms" if tiempo_ejecucion_ms < 1000 else f"{tiempo_ejecucion_ms/1000:.1f}s"
            mensaje += f"\nTiempo transcurrido: {tiempo_str}"
        
        return mensaje
    
    def _generar_mensaje_motor(self, tipo_evento: str, razon: str = None) -> str:
        """Genera el mensaje para notificación de motor"""
        ahora = datetime.now().strftime("%H:%M:%S")
        
        mensajes = {
            "iniciado": f"El motor de controles se ha iniciado a las {ahora}",
            "detenido": f"El motor de controles se ha detenido a las {ahora}",
            "parado": f"El motor de controles se ha detenido inesperadamente a las {ahora}"
        }
        
        mensaje = mensajes.get(tipo_evento, f"Evento del motor: {tipo_evento} a las {ahora}")
        
        if razon:
            mensaje += f"\nRazón: {razon}"
        
        return mensaje
    
    def listar_archivos_notificacion(self, carpeta_origen: str) -> list:
        """
        Lista todos los archivos de notificación en una carpeta
        
        Args:
            carpeta_origen: Ruta de la carpeta a examinar
            
        Returns:
            list: Lista de rutas de archivos de notificación
        """
        try:
            if not os.path.exists(carpeta_origen):
                return []
            
            archivos = []
            for archivo in os.listdir(carpeta_origen):
                if archivo.startswith('notif_') and archivo.endswith('.json'):
                    ruta_completa = os.path.join(carpeta_origen, archivo)
                    archivos.append(ruta_completa)
            
            # Ordenar por fecha de modificación (más antiguos primero)
            archivos.sort(key=lambda x: os.path.getmtime(x))
            
            return archivos
            
        except Exception as e:
            self.logger.error(f"Error al listar archivos de notificación: {e}")
            return []
    
    def leer_archivo_notificacion(self, ruta_archivo: str) -> Optional[Dict[str, Any]]:
        """
        Lee y parsea un archivo de notificación
        
        Args:
            ruta_archivo: Ruta del archivo a leer
            
        Returns:
            dict: Datos de la notificación o None si hay error
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            return datos
            
        except Exception as e:
            self.logger.error(f"Error al leer archivo de notificación {ruta_archivo}: {e}")
            return None
    
    def eliminar_archivo_notificacion(self, ruta_archivo: str) -> bool:
        """
        Elimina un archivo de notificación después de procesarlo
        
        Args:
            ruta_archivo: Ruta del archivo a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            os.remove(ruta_archivo)
            self.logger.info(f"Archivo de notificación eliminado: {ruta_archivo}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al eliminar archivo de notificación {ruta_archivo}: {e}")
            return False