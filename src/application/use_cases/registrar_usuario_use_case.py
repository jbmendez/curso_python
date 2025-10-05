"""
Caso de uso: Registrar Usuario

Los casos de uso encapsulan la lógica de aplicación específica
y orquestan las operaciones entre las diferentes capas.
"""
from datetime import datetime
from typing import List
from src.domain.entities.usuario import Usuario
from src.domain.repositories.usuario_repository import UsuarioRepository
from src.domain.services.usuario_service import UsuarioService
from src.application.dto.usuario_dto import CrearUsuarioDTO, UsuarioResponseDTO


class RegistrarUsuarioUseCase:
    """Caso de uso para registrar un nuevo usuario"""
    
    def __init__(
        self, 
        usuario_repository: UsuarioRepository,
        usuario_service: UsuarioService
    ):
        self._usuario_repository = usuario_repository
        self._usuario_service = usuario_service
    
    def ejecutar(self, datos: CrearUsuarioDTO) -> UsuarioResponseDTO:
        """Ejecuta el caso de uso de registro de usuario"""
        
        # Crear entidad usuario
        usuario = Usuario(
            nombre=datos.nombre,
            email=datos.email,
            fecha_creacion=datetime.now(),
            activo=True
        )
        
        # Validar reglas de negocio
        errores = self._usuario_service.validar_usuario_para_registro(usuario)
        if errores:
            raise ValueError(f"Errores de validación: {', '.join(errores)}")
        
        # Guardar usuario
        usuario_guardado = self._usuario_repository.guardar(usuario)
        
        # Retornar DTO de respuesta
        return UsuarioResponseDTO(
            id=usuario_guardado.id,
            nombre=usuario_guardado.nombre,
            email=usuario_guardado.email,
            fecha_creacion=usuario_guardado.fecha_creacion,
            activo=usuario_guardado.activo
        )