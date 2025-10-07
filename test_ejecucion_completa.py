#!/usr/bin/env python3
"""
Script para probar la ejecución de consultas después de las correcciones
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.infrastructure.repositories.sqlite_consulta_control_repository import SQLiteConsultaControlRepository
from src.domain.services.ejecucion_control_service import EjecucionControlService

def test_ejecucion_control():
    print("🧪 Probando ejecución de control con consultas asociadas...")
    
    # Configurar repositorios
    control_repo = SQLiteControlRepository("sistema_controles.db")
    conexion_repo = SQLiteConexionRepository("sistema_controles.db")
    parametro_repo = SQLiteParametroRepository("sistema_controles.db")
    consulta_repo = SQLiteConsultaRepository("sistema_controles.db")
    referente_repo = SQLiteReferenteRepository("sistema_controles.db")
    consulta_control_repo = SQLiteConsultaControlRepository("sistema_controles.db")
    
    # Crear servicio de ejecución
    ejecucion_service = EjecucionControlService(
        control_repo, parametro_repo, consulta_repo, referente_repo, conexion_repo, consulta_control_repo
    )
    
    # Obtener control ID 2
    control = control_repo.obtener_por_id(2)
    if not control:
        print("❌ No se encontró control con ID 2")
        return
    
    print(f"📋 Control encontrado: {control.nombre}")
    
    # Obtener conexiones disponibles
    conexiones = conexion_repo.obtener_todos()
    if not conexiones:
        print("❌ No hay conexiones disponibles")
        return
    
    conexion = conexiones[0]  # Usar primera conexión disponible
    print(f"🔗 Usando conexión: {conexion.nombre}")
    
    # Verificar asociaciones
    asociaciones = consulta_control_repo.obtener_por_control(control.id)
    print(f"🔗 Asociaciones encontradas: {len(asociaciones)}")
    
    for asoc in asociaciones:
        consulta = consulta_repo.obtener_por_id(asoc.consulta_id)
        disparo_text = "SÍ" if asoc.es_disparo else "NO"
        print(f"   - Consulta: {consulta.nombre if consulta else 'N/A'}, Disparo: {disparo_text}, Orden: {asoc.orden}")
    
    # Ejecutar control
    print("\n⚡ Ejecutando control...")
    try:
        resultado = ejecucion_service.ejecutar_control(
            control=control,
            conexion=conexion,
            mock_execution=True  # Usar simulación
        )
        
        print(f"✅ Estado: {resultado.estado}")
        print(f"📄 Mensaje: {resultado.mensaje}")
        print(f"⏱️ Tiempo: {resultado.tiempo_total_ejecucion_ms:.1f}ms")
        
        if resultado.resultado_consulta_disparo:
            print(f"🎯 Disparo - SQL: {resultado.resultado_consulta_disparo.sql_ejecutado[:100]}...")
            print(f"🎯 Disparo - Filas: {resultado.resultado_consulta_disparo.filas_afectadas}")
        
        if resultado.resultados_consultas_disparadas:
            print(f"📊 Consultas ejecutadas: {len(resultado.resultados_consultas_disparadas)}")
            for i, res in enumerate(resultado.resultados_consultas_disparadas):
                print(f"   {i+1}. {res.consulta_nombre}: {res.filas_afectadas} filas")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ejecucion_control()