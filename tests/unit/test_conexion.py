"""
Test unitario para la entidad Conexión

Ejemplo de testing para las conexiones de base de datos
"""
import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.domain.entities.conexion import Conexion


class TestConexion(unittest.TestCase):
    """Tests para la entidad Conexión"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.conexion_postgres = Conexion(
            id=1,
            nombre="DB Producción",
            base_datos="mi_sistema",
            servidor="localhost",
            puerto=5432,
            usuario="admin",
            contraseña="password123",
            tipo_motor="postgresql",
            activa=True
        )
    
    def test_configuracion_valida(self):
        """Test para validación de configuración"""
        self.assertTrue(self.conexion_postgres.es_configuracion_valida())
        
        # Conexión sin nombre no es válida
        conexion_sin_nombre = Conexion(nombre="")
        self.assertFalse(conexion_sin_nombre.es_configuracion_valida())
        
        # Conexión sin servidor no es válida
        conexion_sin_servidor = Conexion(
            nombre="Test",
            base_datos="db",
            usuario="user"
        )
        self.assertFalse(conexion_sin_servidor.es_configuracion_valida())
    
    def test_string_conexion_postgresql(self):
        """Test para string de conexión PostgreSQL"""
        expected = "postgresql://admin:password123@localhost:5432/mi_sistema"
        self.assertEqual(self.conexion_postgres.obtener_string_conexion(), expected)
        
        # Test con puerto por defecto
        conexion_sin_puerto = Conexion(
            nombre="Test",
            base_datos="test_db",
            servidor="server.com",
            usuario="user",
            contraseña="pass",
            tipo_motor="postgresql"
        )
        expected_default = "postgresql://user:pass@server.com:5432/test_db"
        self.assertEqual(conexion_sin_puerto.obtener_string_conexion(), expected_default)
    
    def test_string_conexion_mysql(self):
        """Test para string de conexión MySQL"""
        conexion_mysql = Conexion(
            nombre="MySQL DB",
            base_datos="aplicacion",
            servidor="mysql.server.com",
            puerto=3306,
            usuario="mysql_user",
            contraseña="mysql_pass",
            tipo_motor="mysql"
        )
        expected = "mysql://mysql_user:mysql_pass@mysql.server.com:3306/aplicacion"
        self.assertEqual(conexion_mysql.obtener_string_conexion(), expected)
    
    def test_string_conexion_sqlite(self):
        """Test para string de conexión SQLite"""
        conexion_sqlite = Conexion(
            nombre="SQLite Local",
            base_datos="/path/to/database.db",
            tipo_motor="sqlite"
        )
        expected = "sqlite:///path/to/database.db"
        self.assertEqual(conexion_sqlite.obtener_string_conexion(), expected)
    
    def test_string_conexion_sqlserver(self):
        """Test para string de conexión SQL Server"""
        conexion_sqlserver = Conexion(
            nombre="SQL Server Prod",
            base_datos="EmpresaDB",
            servidor="sqlserver.empresa.com",
            puerto=1433,
            usuario="sa",
            contraseña="admin123",
            tipo_motor="sqlserver"
        )
        expected = "mssql+pyodbc://sa:admin123@sqlserver.empresa.com:1433/EmpresaDB?driver=ODBC+Driver+17+for+SQL+Server"
        self.assertEqual(conexion_sqlserver.obtener_string_conexion(), expected)
        
        # Test con puerto por defecto para SQL Server
        conexion_sqlserver_default = Conexion(
            nombre="SQL Server Test",
            base_datos="TestDB",
            servidor="sqltest.com",
            usuario="test_user",
            contraseña="test_pass",
            tipo_motor="sqlserver"
        )
        expected_default = "mssql+pyodbc://test_user:test_pass@sqltest.com:1433/TestDB?driver=ODBC+Driver+17+for+SQL+Server"
        self.assertEqual(conexion_sqlserver_default.obtener_string_conexion(), expected_default)
    
    def test_string_conexion_iseries(self):
        """Test para string de conexión iSeries"""
        conexion_iseries = Conexion(
            nombre="AS400 Prod",
            base_datos="MYLIB",
            servidor="as400.empresa.com",
            puerto=446,
            usuario="iseries_user",
            contraseña="iseries_pass",
            tipo_motor="iseries"
        )
        expected = "ibm_db_sa://iseries_user:iseries_pass@as400.empresa.com:446/MYLIB"
        self.assertEqual(conexion_iseries.obtener_string_conexion(), expected)
        
        # Test con puerto por defecto para iSeries
        conexion_iseries_default = Conexion(
            nombre="AS400 Test",
            base_datos="TESTLIB",
            servidor="as400test.com",
            usuario="test_user",
            contraseña="test_pass",
            tipo_motor="iseries"
        )
        expected_default = "ibm_db_sa://test_user:test_pass@as400test.com:446/TESTLIB"
        self.assertEqual(conexion_iseries_default.obtener_string_conexion(), expected_default)
    
    def test_string_conexion_tipo_desconocido(self):
        """Test para tipo de motor desconocido"""
        conexion_desconocida = Conexion(
            nombre="DB Desconocida",
            tipo_motor="oracle"  # No implementado
        )
        self.assertEqual(conexion_desconocida.obtener_string_conexion(), "")
    
    def test_ocultar_contraseña(self):
        """Test para representación sin contraseña"""
        expected = "Conexion(nombre=DB Producción, servidor=localhost, bd=mi_sistema)"
        self.assertEqual(self.conexion_postgres.ocultar_contraseña(), expected)
    
    def test_str_representation(self):
        """Test para representación string (debe ocultar contraseña)"""
        expected = "Conexion(nombre=DB Producción, servidor=localhost, bd=mi_sistema)"
        self.assertEqual(str(self.conexion_postgres), expected)
    
    def test_tipos_motor_soportados(self):
        """Test para verificar que todos los tipos están documentados"""
        # Este test verifica que podemos crear conexiones con todos los tipos mencionados
        tipos_soportados = ["postgresql", "mysql", "sqlite", "sqlserver", "iseries"]
        
        for tipo in tipos_soportados:
            conexion = Conexion(
                nombre=f"Test {tipo}",
                base_datos="test_db",
                servidor="test.server.com",
                usuario="test_user",
                contraseña="test_pass",
                tipo_motor=tipo
            )
            
            # Verificar que se puede crear sin errores
            self.assertEqual(conexion.tipo_motor, tipo)
            
            # Para tipos implementados, verificar que genera string de conexión
            if tipo in ["postgresql", "mysql", "sqlite", "iseries", "sqlserver"]:
                string_conexion = conexion.obtener_string_conexion()
                self.assertNotEqual(string_conexion, "")
            else:
                # Otros tipos no implementados
                string_conexion = conexion.obtener_string_conexion()
                self.assertEqual(string_conexion, "")


if __name__ == '__main__':
    unittest.main()