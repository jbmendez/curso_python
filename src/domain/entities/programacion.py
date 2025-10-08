"""
Entidad Programacion

Representa la configuración de horarios para ejecución automática de controles.
Soporta diferentes tipos de programación: diaria, semanal, mensual, por intervalos.
"""
from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from typing import Optional, List


class TipoProgramacion(Enum):
    """Tipos de programación disponibles"""
    UNICA_VEZ = "unica_vez"           # Ejecutar solo una vez en fecha/hora específica
    DIARIA = "diaria"                 # Ejecutar todos los días a hora específica
    SEMANAL = "semanal"               # Ejecutar días específicos de la semana
    MENSUAL = "mensual"               # Ejecutar días específicos del mes
    INTERVALO = "intervalo"           # Ejecutar cada X minutos/horas


class DiaSemana(Enum):
    """Días de la semana"""
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7


@dataclass
class Programacion:
    """
    Entidad que representa la programación de ejecución automática de un control
    """
    id: Optional[int]
    control_id: int
    nombre: str
    descripcion: str
    tipo_programacion: TipoProgramacion
    activo: bool
    
    # Configuración de horario
    hora_ejecucion: Optional[time]          # Hora específica (HH:MM)
    fecha_inicio: Optional[datetime]         # Fecha de inicio de la programación
    fecha_fin: Optional[datetime]            # Fecha de fin (opcional)
    
    # Para programación semanal
    dias_semana: Optional[List[DiaSemana]]   # [LUNES, MIERCOLES, VIERNES]
    
    # Para programación mensual
    dias_mes: Optional[List[int]]            # [1, 15, 30] - días del mes
    
    # Para programación por intervalo
    intervalo_minutos: Optional[int]         # Cada X minutos
    
    # Control de ejecución
    ultima_ejecucion: Optional[datetime]
    proxima_ejecucion: Optional[datetime]
    total_ejecuciones: int = 0
    
    # Metadatos
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    creado_por: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()
    
    def es_valida(self) -> bool:
        """
        Valida que la programación tenga la configuración necesaria
        según su tipo
        """
        if not self.control_id or not self.nombre:
            return False
        
        if self.tipo_programacion == TipoProgramacion.UNICA_VEZ:
            return self.fecha_inicio is not None and self.hora_ejecucion is not None
        
        elif self.tipo_programacion == TipoProgramacion.DIARIA:
            return self.hora_ejecucion is not None
        
        elif self.tipo_programacion == TipoProgramacion.SEMANAL:
            return (self.hora_ejecucion is not None and 
                   self.dias_semana is not None and 
                   len(self.dias_semana) > 0)
        
        elif self.tipo_programacion == TipoProgramacion.MENSUAL:
            return (self.hora_ejecucion is not None and 
                   self.dias_mes is not None and 
                   len(self.dias_mes) > 0 and
                   all(dia == -1 or (1 <= dia <= 31) for dia in self.dias_mes))
        
        elif self.tipo_programacion == TipoProgramacion.INTERVALO:
            return (self.intervalo_minutos is not None and 
                   self.intervalo_minutos > 0)
        
        return False
    
    def obtener_descripcion_programacion(self) -> str:
        """
        Genera una descripción legible de la programación
        """
        if self.tipo_programacion == TipoProgramacion.UNICA_VEZ:
            return f"Una vez el {self.fecha_inicio.strftime('%d/%m/%Y')} a las {self.hora_ejecucion.strftime('%H:%M')}"
        
        elif self.tipo_programacion == TipoProgramacion.DIARIA:
            return f"Todos los días a las {self.hora_ejecucion.strftime('%H:%M')}"
        
        elif self.tipo_programacion == TipoProgramacion.SEMANAL:
            dias_nombres = [dia.name.capitalize() for dia in self.dias_semana]
            return f"Cada {', '.join(dias_nombres)} a las {self.hora_ejecucion.strftime('%H:%M')}"
        
        elif self.tipo_programacion == TipoProgramacion.MENSUAL:
            dias_str_list = []
            for dia in sorted(self.dias_mes):
                if dia == -1:
                    dias_str_list.append("Fin de mes")
                else:
                    dias_str_list.append(str(dia))
            dias_str = ', '.join(dias_str_list)
            return f"Los días {dias_str} de cada mes a las {self.hora_ejecucion.strftime('%H:%M')}"
        
        elif self.tipo_programacion == TipoProgramacion.INTERVALO:
            if self.intervalo_minutos < 60:
                return f"Cada {self.intervalo_minutos} minutos"
            else:
                horas = self.intervalo_minutos // 60
                minutos = self.intervalo_minutos % 60
                if minutos == 0:
                    return f"Cada {horas} horas"
                else:
                    return f"Cada {horas}h {minutos}m"
        
        return "Programación no definida"
    
    def debe_ejecutarse_ahora(self, fecha_actual: datetime = None) -> bool:
        """
        Determina si el control debe ejecutarse en este momento
        
        Args:
            fecha_actual: Fecha/hora actual (por defecto datetime.now())
            
        Returns:
            bool: True si debe ejecutarse ahora
        """
        if not self.activo:
            return False
        
        if fecha_actual is None:
            fecha_actual = datetime.now()
        
        # Verificar si está dentro del rango de fechas
        if self.fecha_inicio and fecha_actual < self.fecha_inicio:
            return False
        
        if self.fecha_fin and fecha_actual > self.fecha_fin:
            return False
        
        # Verificar según el tipo de programación
        if self.tipo_programacion == TipoProgramacion.UNICA_VEZ:
            return self._debe_ejecutarse_unica_vez(fecha_actual)
        
        elif self.tipo_programacion == TipoProgramacion.DIARIA:
            return self._debe_ejecutarse_diaria(fecha_actual)
        
        elif self.tipo_programacion == TipoProgramacion.SEMANAL:
            return self._debe_ejecutarse_semanal(fecha_actual)
        
        elif self.tipo_programacion == TipoProgramacion.MENSUAL:
            return self._debe_ejecutarse_mensual(fecha_actual)
        
        elif self.tipo_programacion == TipoProgramacion.INTERVALO:
            return self._debe_ejecutarse_intervalo(fecha_actual)
        
        return False
    
    def _debe_ejecutarse_unica_vez(self, fecha_actual: datetime) -> bool:
        """Lógica para ejecución única"""
        if self.total_ejecuciones > 0:
            return False  # Ya se ejecutó
        
        fecha_programada = datetime.combine(
            self.fecha_inicio.date(),
            self.hora_ejecucion
        )
        
        # Permitir ejecución en ventana de 1 minuto
        diferencia = abs((fecha_actual - fecha_programada).total_seconds())
        return diferencia <= 60
    
    def _debe_ejecutarse_diaria(self, fecha_actual: datetime) -> bool:
        """Lógica para ejecución diaria"""
        hora_actual = fecha_actual.time()
        hora_programada = self.hora_ejecucion
        
        # Verificar si es la hora correcta (ventana de 1 minuto)
        diferencia = abs(
            (hora_actual.hour * 60 + hora_actual.minute) - 
            (hora_programada.hour * 60 + hora_programada.minute)
        )
        
        if diferencia > 1:
            return False
        
        # Verificar que no se haya ejecutado hoy
        if self.ultima_ejecucion:
            return self.ultima_ejecucion.date() < fecha_actual.date()
        
        return True
    
    def _debe_ejecutarse_semanal(self, fecha_actual: datetime) -> bool:
        """Lógica para ejecución semanal"""
        dia_actual = DiaSemana(fecha_actual.isoweekday())
        
        if dia_actual not in self.dias_semana:
            return False
        
        return self._debe_ejecutarse_diaria(fecha_actual)
    
    def _debe_ejecutarse_mensual(self, fecha_actual: datetime) -> bool:
        """Lógica para ejecución mensual"""
        dia_actual = fecha_actual.day
        
        # Verificar días específicos
        for dia_programado in self.dias_mes:
            if dia_programado == -1:
                # Fin de mes: verificar si es el último día del mes
                import calendar
                ultimo_dia_mes = calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]
                if dia_actual == ultimo_dia_mes:
                    return self._debe_ejecutarse_diaria(fecha_actual)
            elif dia_actual == dia_programado:
                return self._debe_ejecutarse_diaria(fecha_actual)
        
        return False
    
    def _debe_ejecutarse_intervalo(self, fecha_actual: datetime) -> bool:
        """Lógica para ejecución por intervalo"""
        if not self.ultima_ejecucion:
            return True  # Primera ejecución
        
        minutos_transcurridos = (fecha_actual - self.ultima_ejecucion).total_seconds() / 60
        return minutos_transcurridos >= self.intervalo_minutos
    
    def marcar_ejecutado(self, fecha_ejecucion: datetime = None):
        """
        Marca la programación como ejecutada
        
        Args:
            fecha_ejecucion: Fecha de ejecución (por defecto datetime.now())
        """
        if fecha_ejecucion is None:
            fecha_ejecucion = datetime.now()
        
        self.ultima_ejecucion = fecha_ejecucion
        self.total_ejecuciones += 1
        self.fecha_modificacion = fecha_ejecucion
        
        # Calcular próxima ejecución si es aplicable
        self._calcular_proxima_ejecucion()
    
    def _calcular_proxima_ejecucion(self):
        """Calcula la próxima fecha de ejecución"""
        if not self.activo:
            self.proxima_ejecucion = None
            return
        
        ahora = datetime.now()
        
        if self.tipo_programacion == TipoProgramacion.UNICA_VEZ:
            self.proxima_ejecucion = None  # Solo se ejecuta una vez
        
        elif self.tipo_programacion == TipoProgramacion.DIARIA:
            proxima = datetime.combine(
                ahora.date(),
                self.hora_ejecucion
            )
            if proxima <= ahora:
                proxima = datetime.combine(
                    ahora.date().replace(day=ahora.day + 1),
                    self.hora_ejecucion
                )
            self.proxima_ejecucion = proxima
        
        elif self.tipo_programacion == TipoProgramacion.INTERVALO:
            if self.ultima_ejecucion:
                self.proxima_ejecucion = self.ultima_ejecucion.replace(
                    minute=self.ultima_ejecucion.minute + self.intervalo_minutos
                )
            else:
                self.proxima_ejecucion = ahora
        
        # Para semanal y mensual sería más complejo, lo implementamos después si es necesario