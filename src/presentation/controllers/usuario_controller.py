"""
Controlador para operaciones de Usuario

Los controladores manejan las peticiones HTTP y coordinan
con los casos de uso de la aplicación.
"""
from typing import Dict, Any
from src.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from src.application.dto.usuario_dto import CrearUsuarioDTO


class UsuarioController:
    """Controlador para endpoints de usuario"""
    
    def __init__(self, registrar_usuario_use_case: RegistrarUsuarioUseCase):
        self._registrar_usuario_use_case = registrar_usuario_use_case
    
    def crear_usuario(self, email: str, nombre: str, apellido: str = "") -> Dict[str, Any]:
        """Método simplificado para crear usuario"""
        return self.registrar_usuario({
            'email': email,
            'nombre': f"{nombre} {apellido}".strip()
        })
    
    def registrar_usuario(self, datos_request: Dict[str, Any]) -> Dict[str, Any]:
        """Endpoint para registrar un nuevo usuario"""
        try:
            # Validar datos de entrada
            if not datos_request.get('nombre'):
                return {
                    'error': 'El nombre es obligatorio',
                    'status': 400
                }
            
            if not datos_request.get('email'):
                return {
                    'error': 'El email es obligatorio',
                    'status': 400
                }
            
            # Crear DTO
            dto = CrearUsuarioDTO(
                nombre=datos_request['nombre'],
                email=datos_request['email']
            )
            
            # Ejecutar caso de uso
            usuario_response = self._registrar_usuario_use_case.ejecutar(dto)
            
            # Retornar respuesta exitosa
            return {
                'success': True,
                'data': {
                    'id': usuario_response.id,
                    'nombre': usuario_response.nombre,
                    'email': usuario_response.email,
                    'fecha_creacion': usuario_response.fecha_creacion.isoformat(),
                    'activo': usuario_response.activo
                },
                'status': 201,
                'message': 'Usuario registrado exitosamente'
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'status': 400
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'status': 500
            }