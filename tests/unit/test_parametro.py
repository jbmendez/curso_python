"""
Test unitario para la entidad Parámetro

Ejemplo de testing para las entidades del sistema de controles
"""
import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.entities.parametro import Parametro, TipoParametro


class TestParametro(unittest.TestCase):
    """Tests para la entidad Parámetro"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.parametro = Parametro(
            id=1,
            nombre="fecha_inicio",
            tipo=TipoParametro.DATE,
            descripcion="Fecha de inicio del período",
            obligatorio=True
        )
    
    def test_nombre_valido(self):
        """Test para validación de nombres"""
        # Nombre válido
        self.assertTrue(self.parametro.es_nombre_valido())
        
        # Nombre inválido - con espacios
        parametro_invalido = Parametro(nombre="fecha inicio")
        self.assertFalse(parametro_invalido.es_nombre_valido())
        
        # Nombre inválido - vacío
        parametro_vacio = Parametro(nombre="")
        self.assertFalse(parametro_vacio.es_nombre_valido())
        
        # Nombre inválido - con caracteres especiales
        parametro_especial = Parametro(nombre="fecha-inicio")
        self.assertFalse(parametro_especial.es_nombre_valido())
    
    def test_validar_valor_string(self):
        """Test para validación de valores string"""
        parametro_string = Parametro(
            nombre="nombre",
            tipo=TipoParametro.STRING,
            obligatorio=True
        )
        
        self.assertTrue(parametro_string.validar_valor("Juan"))
        self.assertTrue(parametro_string.validar_valor("123"))
        self.assertFalse(parametro_string.validar_valor(""))  # Obligatorio
    
    def test_validar_valor_integer(self):
        """Test para validación de valores enteros"""
        parametro_int = Parametro(
            nombre="edad",
            tipo=TipoParametro.INTEGER,
            obligatorio=True
        )
        
        self.assertTrue(parametro_int.validar_valor("25"))
        self.assertTrue(parametro_int.validar_valor("-5"))
        self.assertFalse(parametro_int.validar_valor("abc"))
        self.assertFalse(parametro_int.validar_valor("25.5"))
    
    def test_validar_valor_float(self):
        """Test para validación de valores flotantes"""
        parametro_float = Parametro(
            nombre="precio",
            tipo=TipoParametro.FLOAT,
            obligatorio=True
        )
        
        self.assertTrue(parametro_float.validar_valor("25.5"))
        self.assertTrue(parametro_float.validar_valor("25"))
        self.assertTrue(parametro_float.validar_valor("-25.5"))
        self.assertFalse(parametro_float.validar_valor("abc"))
    
    def test_validar_valor_boolean(self):
        """Test para validación de valores booleanos"""
        parametro_bool = Parametro(
            nombre="activo",
            tipo=TipoParametro.BOOLEAN,
            obligatorio=True
        )
        
        self.assertTrue(parametro_bool.validar_valor("true"))
        self.assertTrue(parametro_bool.validar_valor("false"))
        self.assertTrue(parametro_bool.validar_valor("1"))
        self.assertTrue(parametro_bool.validar_valor("0"))
        self.assertFalse(parametro_bool.validar_valor("abc"))
        self.assertFalse(parametro_bool.validar_valor("2"))
    
    def test_parametro_no_obligatorio(self):
        """Test para parámetros no obligatorios"""
        parametro_opcional = Parametro(
            nombre="comentario",
            tipo=TipoParametro.STRING,
            obligatorio=False
        )
        
        # Valor vacío es válido si no es obligatorio
        self.assertTrue(parametro_opcional.validar_valor(""))
        self.assertTrue(parametro_opcional.validar_valor("algún texto"))
    
    def test_str_representation(self):
        """Test para representación string"""
        expected = "Parametro(nombre=fecha_inicio, tipo=date)"
        self.assertEqual(str(self.parametro), expected)
    
    def test_tipos_parametro_enum(self):
        """Test para verificar que todos los tipos están disponibles"""
        tipos_esperados = ["string", "integer", "float", "boolean", "date", "datetime"]
        tipos_disponibles = [tipo.value for tipo in TipoParametro]
        
        for tipo in tipos_esperados:
            self.assertIn(tipo, tipos_disponibles)


if __name__ == '__main__':
    unittest.main()