"""
Caso de uso: Crear Parámetro

Este caso de uso maneja la creación de un nuevo parámetro
"""
from src.domain.entities.parametro import Parametro, TipoParametro
from src.domain.repositories.parametro_repository import ParametroRepository
from src.application.dto.entidades_dto import CrearParametroDTO, ParametroResponseDTO


class CrearParametroUseCase:
    """Caso de uso para crear un nuevo parámetro"""
    
    def __init__(self, parametro_repository: ParametroRepository):
        self._parametro_repository = parametro_repository
    
    def ejecutar(self, datos: CrearParametroDTO) -> ParametroResponseDTO:
        """Ejecuta el caso de uso de creación de parámetro"""
        
        # Verificar que el nombre no exista
        parametro_existente = self._parametro_repository.obtener_por_nombre(datos.nombre)
        if parametro_existente:
            raise ValueError(f"Ya existe un parámetro con el nombre '{datos.nombre}'")
        
        # Validar tipo de parámetro
        try:
            tipo_parametro = TipoParametro(datos.tipo)
        except ValueError:
            raise ValueError(f"Tipo de parámetro inválido: {datos.tipo}")
        
        # Crear entidad parámetro
        parametro = Parametro(
            nombre=datos.nombre,
            tipo=tipo_parametro,
            descripcion=datos.descripcion,
            valor_por_defecto=datos.valor_por_defecto,
            obligatorio=datos.obligatorio
        )
        
        # Validar que el nombre sea válido
        if not parametro.es_nombre_valido():
            raise ValueError(f"El nombre del parámetro '{datos.nombre}' no es válido")
        
        # Guardar parámetro
        parametro_guardado = self._parametro_repository.guardar(parametro)
        
        # Retornar DTO de respuesta
        return ParametroResponseDTO(
            id=parametro_guardado.id,
            nombre=parametro_guardado.nombre,
            tipo=parametro_guardado.tipo.value,
            descripcion=parametro_guardado.descripcion,
            valor_por_defecto=parametro_guardado.valor_por_defecto,
            obligatorio=parametro_guardado.obligatorio
        )