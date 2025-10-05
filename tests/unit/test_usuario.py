"""
Test unitario para la entidad Usuario

Ejemplo de testing para la capa de dominio
"""
import unittest
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path para poder importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.entities.usuario import Usuario


class TestUsuario(unittest.TestCase):
    """Tests para la entidad Usuario"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.usuario = Usuario(
            id=1,
            nombre="Juan Pérez",
            email="juan@ejemplo.com",
            fecha_creacion=datetime.now(),
            activo=True
        )
    
    def test_activar_usuario(self):
        """Test para activar usuario"""
        self.usuario.activo = False
        self.usuario.activar()
        self.assertTrue(self.usuario.activo)
    
    def test_desactivar_usuario(self):
        """Test para desactivar usuario"""
        self.usuario.desactivar()
        self.assertFalse(self.usuario.activo)
    
    def test_email_valido(self):
        """Test para validación de email"""
        self.assertTrue(self.usuario.es_email_valido())
        
        self.usuario.email = "email_invalido"
        self.assertFalse(self.usuario.es_email_valido())
    
    def test_str_representation(self):
        """Test para representación string"""
        expected = "Usuario(id=1, nombre=Juan Pérez, email=juan@ejemplo.com)"
        self.assertEqual(str(self.usuario), expected)


if __name__ == '__main__':
    unittest.main()