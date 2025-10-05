"""
Servicio de dominio para gestión de Controles

Este servicio contiene la lógica de negocio compleja relacionada con controles
que no pertenece a una entidad específica.
"""
from typing import List, Dict, Any
from src.domain.entities.control import Control
from src.domain.entities.consulta import Consulta
from src.domain.entities.conexion import Conexion
from src.domain.repositories.control_repository import ControlRepository
from src.domain.repositories.consulta_repository import ConsultaRepository
from src.domain.repositories.conexion_repository import ConexionRepository
from src.domain.repositories.parametro_repository import ParametroRepository
from src.domain.repositories.referente_repository import ReferenteRepository


class ControlService:
    """Servicio de dominio para operaciones complejas de controles"""
    
    def __init__(
        self,
        control_repository: ControlRepository,
        consulta_repository: ConsultaRepository,
        conexion_repository: ConexionRepository,
        parametro_repository: ParametroRepository,
        referente_repository: ReferenteRepository
    ):
        self._control_repository = control_repository
        self._consulta_repository = consulta_repository
        self._conexion_repository = conexion_repository
        self._parametro_repository = parametro_repository
        self._referente_repository = referente_repository
    
    def validar_control_para_creacion(self, control: Control) -> List[str]:
        """Valida si un control puede ser creado"""
        errores = []
        
        # Validaciones básicas de la entidad
        if not control.es_configuracion_valida():
            errores.append("La configuración básica del control no es válida")
        
        # Verificar que la conexión existe y es válida
        if control.conexion_id:
            conexion = self._conexion_repository.obtener_por_id(control.conexion_id)
            if not conexion:
                errores.append("La conexión especificada no existe")
            elif not conexion.activa:
                errores.append("La conexión especificada no está activa")
            elif not conexion.es_configuracion_valida():
                errores.append("La configuración de la conexión no es válida")
        
        # Verificar que la consulta de disparo existe y es válida
        if control.consulta_disparo_id:
            consulta = self._consulta_repository.obtener_por_id(control.consulta_disparo_id)
            if not consulta:
                errores.append("La consulta de disparo especificada no existe")
            elif not consulta.activa:
                errores.append("La consulta de disparo no está activa")
            elif not consulta.es_sql_valido():
                errores.append("El SQL de la consulta de disparo no es válido")
            elif consulta.es_consulta_peligrosa():
                errores.append("La consulta de disparo contiene operaciones peligrosas")
        
        # Verificar que las consultas a disparar existen y son válidas
        if control.consultas_a_disparar_ids:
            consultas = self._consulta_repository.obtener_por_ids(control.consultas_a_disparar_ids)
            if len(consultas) != len(control.consultas_a_disparar_ids):
                errores.append("Algunas consultas a disparar no existen")
            else:
                for consulta in consultas:
                    if not consulta.activa:
                        errores.append(f"La consulta '{consulta.nombre}' no está activa")
                    if not consulta.es_sql_valido():
                        errores.append(f"El SQL de la consulta '{consulta.nombre}' no es válido")
                    if consulta.es_consulta_peligrosa():
                        errores.append(f"La consulta '{consulta.nombre}' contiene operaciones peligrosas")
        
        # Verificar que los parámetros existen
        if control.parametros_ids:
            parametros = self._parametro_repository.obtener_por_ids(control.parametros_ids)
            if len(parametros) != len(control.parametros_ids):
                errores.append("Algunos parámetros especificados no existen")
        
        # Verificar que los referentes existen
        if control.referentes_ids:
            referentes = self._referente_repository.obtener_por_ids(control.referentes_ids)
            if len(referentes) != len(control.referentes_ids):
                errores.append("Algunos referentes especificados no existen")
        
        return errores
    
    def nombre_control_disponible(self, nombre: str, control_id: int = None) -> bool:
        """Verifica si un nombre de control está disponible"""
        control_existente = self._control_repository.obtener_por_nombre(nombre)
        if not control_existente:
            return True
        
        # Si estamos actualizando, permitir el mismo nombre si es el mismo control
        return control_existente.id == control_id
    
    def cargar_control_completo(self, control_id: int) -> Control:
        """Carga un control con todas sus relaciones"""
        control = self._control_repository.obtener_por_id(control_id)
        if not control:
            raise ValueError(f"Control con ID {control_id} no encontrado")
        
        return self._control_repository.cargar_relaciones(control)
    
    def obtener_controles_ejecutables(self) -> List[Control]:
        """Obtiene todos los controles que pueden ejecutarse"""
        controles_activos = self._control_repository.obtener_activos()
        controles_ejecutables = []
        
        for control in controles_activos:
            control_completo = self.cargar_control_completo(control.id)
            if control_completo.puede_ejecutarse():
                controles_ejecutables.append(control_completo)
        
        return controles_ejecutables
    
    def validar_parametros_control(self, control: Control, valores_parametros: Dict[str, str]) -> List[str]:
        """Valida los parámetros de un control antes de la ejecución"""
        # Cargar el control completo si no tiene las relaciones cargadas
        if not control.parametros:
            control = self.cargar_control_completo(control.id)
        
        return control.validar_parametros_completos(valores_parametros)