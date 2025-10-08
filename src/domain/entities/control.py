"""
Entidad Control

Representa un control que se ejecuta sobre una base de datos
con consultas SQL y parámetros
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from .parametro import Parametro
from .consulta import Consulta
from .conexion import Conexion
from .referente import Referente


@dataclass
class Control:
    """Entidad Control - Representa un control SQL con sus consultas y parámetros"""
    
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    activo: bool = True
    fecha_creacion: Optional[datetime] = None
    
    # Configuración del control
    disparar_si_hay_datos: bool = True  # Si True, dispara cuando HAY datos; si False, cuando NO hay datos
    
    # Relaciones
    conexion_id: Optional[int] = None
    consulta_disparo_id: Optional[int] = None
    
    # Listas de IDs para las relaciones many-to-many
    parametros_ids: List[int] = field(default_factory=list)
    consultas_a_disparar_ids: List[int] = field(default_factory=list)
    referentes_ids: List[int] = field(default_factory=list)
    
    # Objetos relacionados (se cargarán desde repositorios)
    conexion: Optional[Conexion] = None
    consulta_disparo: Optional[Consulta] = None
    parametros: List[Parametro] = field(default_factory=list)
    consultas_a_disparar: List[Consulta] = field(default_factory=list)
    referentes: List[Referente] = field(default_factory=list)
    
    # Lista de programaciones (se carga desde repositorio)
    programaciones: List = field(default_factory=list)  # List[Programacion] - evitamos import circular
    
    def es_configuracion_valida(self) -> bool:
        """Valida que el control tenga una configuración válida para ejecución"""
        if not self.nombre.strip():
            return False
        
        if not self.conexion_id:
            return False
            
        if not self.consulta_disparo_id:
            return False
            
        if not self.consultas_a_disparar_ids:
            return False
            
        return True
    
    def es_configuracion_basica_valida(self) -> bool:
        """Valida configuración mínima para creación de control"""
        if not self.nombre.strip():
            return False
        
        if not self.conexion_id:
            return False
            
        return True
    
    def obtener_parametros_requeridos(self) -> List[str]:
        """Obtiene los nombres de todos los parámetros requeridos por las consultas"""
        parametros_requeridos = set()
        
        # Parámetros de la consulta de disparo
        if self.consulta_disparo:
            parametros_requeridos.update(self.consulta_disparo.obtener_parametros_en_sql())
        
        # Parámetros de las consultas a disparar
        for consulta in self.consultas_a_disparar:
            parametros_requeridos.update(consulta.obtener_parametros_en_sql())
        
        return list(parametros_requeridos)
    
    def validar_parametros_completos(self, valores_parametros: Dict[str, str]) -> List[str]:
        """Valida que todos los parámetros requeridos estén presentes y sean válidos"""
        errores = []
        parametros_requeridos = self.obtener_parametros_requeridos()
        
        # Verificar parámetros faltantes
        for param_nombre in parametros_requeridos:
            if param_nombre not in valores_parametros:
                errores.append(f"Falta el parámetro requerido: {param_nombre}")
                continue
            
            # Buscar la definición del parámetro para validar el tipo
            param_def = next((p for p in self.parametros if p.nombre == param_nombre), None)
            if param_def and not param_def.validar_valor(valores_parametros[param_nombre]):
                errores.append(f"Valor inválido para el parámetro {param_nombre}")
        
        return errores
    
    def puede_ejecutarse(self) -> bool:
        """Verifica si el control puede ejecutarse"""
        return (self.activo and 
                self.es_configuracion_valida() and 
                self.conexion is not None and 
                self.consulta_disparo is not None)
    
    def agregar_parametro(self, parametro_id: int) -> None:
        """Agrega un parámetro al control"""
        if parametro_id not in self.parametros_ids:
            self.parametros_ids.append(parametro_id)
    
    def agregar_consulta_a_disparar(self, consulta_id: int) -> None:
        """Agrega una consulta a la lista de consultas a disparar"""
        if consulta_id not in self.consultas_a_disparar_ids:
            self.consultas_a_disparar_ids.append(consulta_id)
    
    def agregar_referente(self, referente_id: int) -> None:
        """Agrega un referente al control"""
        if referente_id not in self.referentes_ids:
            self.referentes_ids.append(referente_id)
    
    def tiene_programaciones_activas(self) -> bool:
        """Verifica si el control tiene programaciones activas"""
        return any(prog.activo for prog in self.programaciones)
    
    def obtener_programaciones_activas(self) -> List:
        """Obtiene solo las programaciones activas del control"""
        return [prog for prog in self.programaciones if prog.activo]
    
    def obtener_proxima_ejecucion_programada(self):
        """Obtiene la fecha de la próxima ejecución programada"""
        programaciones_activas = self.obtener_programaciones_activas()
        if not programaciones_activas:
            return None
        
        proximas_ejecuciones = [
            prog.proxima_ejecucion 
            for prog in programaciones_activas 
            if prog.proxima_ejecucion
        ]
        
        if not proximas_ejecuciones:
            return None
        
        return min(proximas_ejecuciones)
    
    def debe_ejecutarse_automaticamente(self, fecha_actual: datetime = None) -> bool:
        """
        Verifica si el control debe ejecutarse automáticamente ahora
        
        Args:
            fecha_actual: Fecha/hora actual (por defecto datetime.now())
            
        Returns:
            bool: True si debe ejecutarse por alguna programación
        """
        if not self.activo or not self.puede_ejecutarse():
            return False
        
        return any(
            prog.debe_ejecutarse_ahora(fecha_actual) 
            for prog in self.obtener_programaciones_activas()
        )
    
    def __str__(self) -> str:
        return f"Control(id={self.id}, nombre={self.nombre}, activo={self.activo})"