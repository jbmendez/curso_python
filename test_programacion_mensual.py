#!/usr/bin/env python3
"""
Script de prueba para programación mensual
"""
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath('src'))

from domain.entities.programacion import TipoProgramacion, Programacion
from datetime import datetime, time

def test_programacion_mensual():
    """Prueba la creación de una programación mensual"""
    print("🧪 Probando programación mensual...")
    
    try:
        # Crear programación mensual
        programacion = Programacion(
            id=None,
            control_id=1,
            nombre="Test Mensual",
            descripcion="Programación de prueba mensual",
            tipo_programacion=TipoProgramacion.MENSUAL,
            activo=True,
            hora_ejecucion=time(14, 30),
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            dias_semana=None,
            dias_mes=[1, 15, 30],  # Días 1, 15 y 30 del mes
            intervalo_minutos=None,
            ultima_ejecucion=None,
            proxima_ejecucion=None,
            total_ejecuciones=0,
            fecha_creacion=datetime.now(),
            fecha_modificacion=None,
            creado_por="test"
        )
        
        print(f"✅ Programación creada: {programacion.nombre}")
        print(f"   Tipo: {programacion.tipo_programacion.value}")
        print(f"   Días del mes: {programacion.dias_mes}")
        print(f"   Hora: {programacion.hora_ejecucion}")
        
        # Verificar validación
        if programacion.es_valida():
            print("✅ Programación es válida")
        else:
            print("❌ Programación NO es válida")
        
        # Probar descripción
        descripcion = programacion.obtener_descripcion_programacion()
        print(f"📝 Descripción: {descripcion}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_programacion_mensual()