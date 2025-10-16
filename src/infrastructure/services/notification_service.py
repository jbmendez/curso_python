"""
Servicio de notificaciones para Windows

Proporciona funcionalidad para mostrar notificaciones del sistema
cuando se ejecutan controles o se producen eventos importantes.
"""
import logging
from typing import Optional
from datetime import datetime

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    notification = None


class WindowsNotificationService:
    """Servicio para mostrar notificaciones de Windows"""
    
    def __init__(self):
        """Inicializa el servicio de notificaciones"""
        self.logger = logging.getLogger(__name__)
        
        if NOTIFICATIONS_AVAILABLE:
            self.logger.info("Servicio de notificaciones inicializado con plyer")
        else:
            self.logger.warning("plyer no está disponible. Notificaciones deshabilitadas.")
    
    def is_available(self) -> bool:
        """Verifica si las notificaciones están disponibles"""
        return NOTIFICATIONS_AVAILABLE
    
    def _truncar_texto(self, texto: str, max_length: int) -> str:
        """
        Trunca el texto si excede la longitud máxima
        
        Args:
            texto: Texto a truncar
            max_length: Longitud máxima permitida
            
        Returns:
            str: Texto truncado si es necesario
        """
        if len(texto) <= max_length:
            return texto
        return texto[:max_length-3] + "..."
    
    def _truncar_control_nombre(self, control_nombre: str) -> str:
        """
        Trunca nombres de control largos para títulos de notificación
        
        Args:
            control_nombre: Nombre del control
            
        Returns:
            str: Nombre truncado apropiado para títulos
        """
        # Límite conservador para títulos (Windows tiene límite ~64 chars)
        max_title_length = 40
        return self._truncar_texto(control_nombre, max_title_length)
    
    def _mostrar_notificacion(self, titulo: str, mensaje: str, timeout: int = 10) -> bool:
        """
        Método interno para mostrar notificaciones
        
        Args:
            titulo: Título de la notificación
            mensaje: Mensaje de la notificación
            timeout: Tiempo en segundos que se muestra la notificación
            
        Returns:
            bool: True si se mostró exitosamente
        """
        if not self.is_available():
            self.logger.debug("Notificaciones no disponibles")
            return False
        
        try:
            # Aplicar límites de caracteres para evitar errores
            titulo_truncado = self._truncar_texto(titulo, 60)  # Límite conservador para títulos
            mensaje_truncado = self._truncar_texto(mensaje, 200)  # Límite para mensajes
            
            notification.notify(
                title=titulo_truncado,
                message=mensaje_truncado,
                timeout=timeout,
                app_name="Motor de Controles"
            )
            return True
        except Exception as e:
            self.logger.error(f"Error al mostrar notificación: {e}")
            return False
    
    def mostrar_control_disparado(
        self,
        control_nombre: str,
        filas_procesadas: int,
        tiempo_ejecucion_ms: float,
        mensaje_adicional: str = None
    ) -> bool:
        """
        Muestra una notificación cuando un control se dispara exitosamente
        
        Args:
            control_nombre: Nombre del control que se disparó
            filas_procesadas: Número de filas procesadas
            tiempo_ejecucion_ms: Tiempo de ejecución en milisegundos
            mensaje_adicional: Mensaje adicional opcional
            
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        # Formatear tiempo
        tiempo_str = f"{tiempo_ejecucion_ms:.0f}ms" if tiempo_ejecucion_ms < 1000 else f"{tiempo_ejecucion_ms/1000:.1f}s"
        
        # Crear mensaje
        mensaje = f"Procesadas {filas_procesadas} filas en {tiempo_str}"
        if mensaje_adicional:
            mensaje += f"\n{mensaje_adicional}"
        
        # Truncar nombre del control para el título
        control_truncado = self._truncar_control_nombre(control_nombre)
        titulo = f"✅ Control: {control_truncado}"
        
        resultado = self._mostrar_notificacion(titulo, mensaje, timeout=10)
        if resultado:
            self.logger.info(f"Notificación mostrada para control: {control_nombre}")
        
        return resultado
    
    def mostrar_control_error(
        self,
        control_nombre: str,
        error_mensaje: str,
        tiempo_ejecucion_ms: float = None
    ) -> bool:
        """
        Muestra una notificación cuando un control falla
        
        Args:
            control_nombre: Nombre del control que falló
            error_mensaje: Mensaje de error
            tiempo_ejecucion_ms: Tiempo de ejecución en milisegundos
            
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        # Limitar longitud del mensaje de error
        error_corto = error_mensaje[:100] + "..." if len(error_mensaje) > 100 else error_mensaje
        
        mensaje = f"Error: {error_corto}"
        if tiempo_ejecucion_ms:
            tiempo_str = f"{tiempo_ejecucion_ms:.0f}ms" if tiempo_ejecucion_ms < 1000 else f"{tiempo_ejecucion_ms/1000:.1f}s"
            mensaje += f"\nTiempo: {tiempo_str}"
        
        # Truncar nombre del control para el título
        control_truncado = self._truncar_control_nombre(control_nombre)
        titulo = f"❌ Error: {control_truncado}"
        
        resultado = self._mostrar_notificacion(titulo, mensaje, timeout=15)
        if resultado:
            self.logger.info(f"Notificación de error mostrada para control: {control_nombre}")
        
        return resultado
    
    def mostrar_motor_iniciado(self) -> bool:
        """
        Muestra una notificación cuando el motor se inicia
        
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        ahora = datetime.now().strftime("%H:%M:%S")
        titulo = "🚀 Motor de Controles Iniciado"
        mensaje = f"Sistema iniciado a las {ahora}\nEjecutando controles automáticamente..."
        
        resultado = self._mostrar_notificacion(titulo, mensaje, timeout=8)
        if resultado:
            self.logger.info("Notificación de inicio de motor mostrada")
        
        return resultado
    
    def mostrar_motor_detenido(self) -> bool:
        """
        Muestra una notificación cuando el motor se detiene
        
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        ahora = datetime.now().strftime("%H:%M:%S")
        titulo = "⏹️ Motor de Controles Detenido"
        mensaje = f"Sistema detenido a las {ahora}"
        
        resultado = self._mostrar_notificacion(titulo, mensaje, timeout=5)
        if resultado:
            self.logger.info("Notificación de detención de motor mostrada")
        
        return resultado
    
    def mostrar_motor_parado(self, razon: str) -> bool:
        """
        Muestra una notificación cuando el motor se para por una razón específica
        
        Args:
            razon: Razón por la cual se paró el motor
            
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        razon_corta = razon[:150] + "..." if len(razon) > 150 else razon
        titulo = "🛑 Motor Detenido"
        
        resultado = self._mostrar_notificacion(titulo, razon_corta, timeout=10)
        if resultado:
            self.logger.info("Notificación de motor detenido mostrada")
        
        return resultado
    
    def mostrar_resumen_ejecucion(
        self,
        total_controles: int,
        controles_disparados: int,
        controles_error: int,
        tiempo_total_ms: float
    ) -> bool:
        """
        Muestra un resumen de la ejecución de controles
        
        Args:
            total_controles: Total de controles verificados
            controles_disparados: Controles que se dispararon
            controles_error: Controles con error
            tiempo_total_ms: Tiempo total de ejecución
            
        Returns:
            bool: True si la notificación se mostró exitosamente
        """
        tiempo_str = f"{tiempo_total_ms:.0f}ms" if tiempo_total_ms < 1000 else f"{tiempo_total_ms/1000:.1f}s"
        
        mensaje = f"Total: {total_controles} | Disparados: {controles_disparados}"
        if controles_error > 0:
            mensaje += f" | Errores: {controles_error}"
        mensaje += f"\nTiempo: {tiempo_str}"
        
        # Determinar título según resultados
        if controles_error > 0:
            titulo = "⚠️ Ejecución Completada con Errores"
        elif controles_disparados > 0:
            titulo = "✅ Ejecución Completada"
        else:
            titulo = "ℹ️ Ejecución Completada"
        
        resultado = self._mostrar_notificacion(titulo, mensaje, timeout=8)
        if resultado:
            self.logger.info(f"Notificación de resumen mostrada: {controles_disparados}/{total_controles} disparados")
        
        return resultado