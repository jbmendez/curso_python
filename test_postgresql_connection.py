"""
Script de prueba para validar la funcionalidad de conexión PostgreSQL
"""
import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.domain.entities.conexion import Conexion
from src.infrastructure.services.postgresql_conexion_test import PostgreSQLConexionTest
from src.domain.services.conexion_test_service import ConexionTestFactory

def main():
    print("🔍 Prueba de Servicios de Conexión PostgreSQL")
    print("=" * 50)
    
    # Inicializar y registrar servicio
    postgresql_service = PostgreSQLConexionTest()
    ConexionTestFactory.registrar_servicio(
        postgresql_service.tipos_soportados(), 
        postgresql_service
    )
    
    print(f"✅ Tipos soportados: {postgresql_service.tipos_soportados()}")
    print(f"✅ Servicios registrados en factory: {ConexionTestFactory.tipos_soportados()}")
    
    # Crear conexión de prueba
    conexion_prueba = Conexion(
        id=None,
        nombre="test_connection",
        base_datos="postgres",  # Base de datos por defecto
        servidor="localhost",
        puerto=5432,
        usuario="postgres",
        contraseña="password",  # Cambia esto por tu contraseña
        tipo_motor="postgresql",
        activa=True
    )
    
    print(f"\n🔌 Probando conexión a:")
    print(f"   Servidor: {conexion_prueba.servidor}:{conexion_prueba.puerto}")
    print(f"   Base de datos: {conexion_prueba.base_datos}")
    print(f"   Usuario: {conexion_prueba.usuario}")
    
    # Obtener servicio del factory
    servicio = ConexionTestFactory.obtener_servicio("postgresql")
    
    if servicio:
        print(f"\n✅ Servicio obtenido del factory: {type(servicio).__name__}")
        
        # Probar conexión
        resultado = servicio.probar_conexion(conexion_prueba)
        
        print(f"\n📊 Resultado:")
        print(f"   Exitosa: {resultado.exitosa}")
        print(f"   Mensaje: {resultado.mensaje}")
        if resultado.tiempo_respuesta:
            print(f"   Tiempo: {resultado.tiempo_respuesta:.2f}s")
        if resultado.version_servidor:
            print(f"   Versión: {resultado.version_servidor}")
        if resultado.detalles_error:
            print(f"   Error: {resultado.detalles_error}")
    else:
        print("❌ No se pudo obtener el servicio del factory")

if __name__ == "__main__":
    main()