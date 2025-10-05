"""
Test unitario para la entidad Control

Ejemplo de testing para las nuevas entidades del dominio
"""
import unittest
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.entities.control import Control
from src.domain.entities.parametro import Parametro, TipoParametro
from src.domain.entities.consulta import Consulta


class TestControl(unittest.TestCase):
    """Tests para la entidad Control"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.control = Control(
            id=1,
            nombre="Control Test",
            descripcion="Un control de prueba",
            activo=True,
            fecha_creacion=datetime.now(),
            disparar_si_hay_datos=True,
            conexion_id=1,
            consulta_disparo_id=1,
            consultas_a_disparar_ids=[2, 3],
            parametros_ids=[1, 2],
            referentes_ids=[1]
        )
    
    def test_configuracion_valida(self):
        """Test para validación de configuración"""
        self.assertTrue(self.control.es_configuracion_valida())
        
        # Control sin nombre no es válido
        control_sin_nombre = Control(nombre="")
        self.assertFalse(control_sin_nombre.es_configuracion_valida())
        
        # Control sin conexión no es válido
        control_sin_conexion = Control(nombre="Test")
        self.assertFalse(control_sin_conexion.es_configuracion_valida())
    
    def test_agregar_parametro(self):
        """Test para agregar parámetros"""
        # Agregar nuevo parámetro
        self.control.agregar_parametro(3)
        self.assertIn(3, self.control.parametros_ids)
        
        # No duplicar parámetros
        self.control.agregar_parametro(3)
        self.assertEqual(self.control.parametros_ids.count(3), 1)
    
    def test_agregar_consulta_a_disparar(self):
        """Test para agregar consultas a disparar"""
        self.control.agregar_consulta_a_disparar(4)
        self.assertIn(4, self.control.consultas_a_disparar_ids)
    
    def test_agregar_referente(self):
        """Test para agregar referentes"""
        self.control.agregar_referente(2)
        self.assertIn(2, self.control.referentes_ids)
    
    def test_obtener_parametros_requeridos_con_consultas(self):
        """Test para obtener parámetros requeridos cuando hay consultas cargadas"""
        # Crear consultas de ejemplo
        consulta_disparo = Consulta(
            id=1,
            nombre="Consulta Disparo",
            sql="SELECT * FROM tabla WHERE fecha = :fecha AND estado = :estado"
        )
        
        consulta_a_disparar = Consulta(
            id=2,
            nombre="Consulta A Disparar",
            sql="SELECT * FROM otra_tabla WHERE id = :id"
        )
        
        # Asignar consultas al control
        self.control.consulta_disparo = consulta_disparo
        self.control.consultas_a_disparar = [consulta_a_disparar]
        
        # Obtener parámetros requeridos
        parametros_requeridos = self.control.obtener_parametros_requeridos()
        
        # Verificar que se encontraron los parámetros
        self.assertIn('fecha', parametros_requeridos)
        self.assertIn('estado', parametros_requeridos)
        self.assertIn('id', parametros_requeridos)
    
    def test_puede_ejecutarse(self):
        """Test para verificar si un control puede ejecutarse"""
        # Sin objetos relacionados, no puede ejecutarse
        self.assertFalse(self.control.puede_ejecutarse())
        
        # Agregar objetos mock
        self.control.conexion = type('MockConexion', (), {})()
        self.control.consulta_disparo = type('MockConsulta', (), {})()
        
        # Ahora debería poder ejecutarse
        self.assertTrue(self.control.puede_ejecutarse())
        
        # Si se desactiva, no puede ejecutarse
        self.control.activo = False
        self.assertFalse(self.control.puede_ejecutarse())
    
    def test_str_representation(self):
        """Test para representación string"""
        expected = "Control(id=1, nombre=Control Test, activo=True)"
        self.assertEqual(str(self.control), expected)


if __name__ == '__main__':
    unittest.main()