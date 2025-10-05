"""
Servicio de dominio para Usuario

Los servicios de dominio contienen lógica de negocio que no pertenece
a una entidad específica o que involucra múltiples entidades.
"""
from typing import List
from src.domain.entities.usuario import Usuario
from src.domain.repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    """Servicio de dominio para operaciones complejas de usuario"""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self._usuario_repository = usuario_repository
    
    def email_esta_disponible(self, email: str) -> bool:
        """Verifica si un email está disponible para registro"""
        usuario_existente = self._usuario_repository.obtener_por_email(email)
        return usuario_existente is None
    
    def validar_usuario_para_registro(self, usuario: Usuario) -> List[str]:
        """Valida si un usuario puede ser registrado"""
        errores = []
        
        if not usuario.nombre.strip():
            errores.append("El nombre es obligatorio")
        
        if not usuario.es_email_valido():
            errores.append("El formato del email no es válido")
        
        if not self.email_esta_disponible(usuario.email):
            errores.append("El email ya está registrado")
        
        return errores