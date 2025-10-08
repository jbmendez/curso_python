#!/usr/bin/env python3
"""
Script de prueba para validación de programación mensual con fin de mes
"""
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath('src'))

from src.domain.entities.programacion import TipoProgramacion, Programacion
from datetime import datetime, time

def test_validacion_fin_de_mes():
    """Prueba la validación de programación mensual con fin de mes"""
    print("🧪 Probando validación programación mensual con fin de mes...")
    
    try:
        # Crear programación mensual solo con fin de mes
        programacion_fin_mes = Programacion(
            id=None,
            control_id=1,
            nombre="Test Fin de Mes",
            descripcion="Solo fin de mes",
            tipo_programacion=TipoProgramacion.MENSUAL,
            activo=True,
            hora_ejecucion=time(14, 30),
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            dias_semana=None,
            dias_mes=[-1],  # Solo fin de mes
            intervalo_minutos=None,
            ultima_ejecucion=None,
            proxima_ejecucion=None,
            total_ejecuciones=0,
            fecha_creacion=datetime.now(),
            fecha_modificacion=None,
            creado_por="test"
        )
        
        print(f"✅ Programación creada: {programacion_fin_mes.nombre}")
        print(f"   Días del mes: {programacion_fin_mes.dias_mes}")
        
        # Verificar validación
        if programacion_fin_mes.es_valida():
            print("✅ Programación FIN DE MES es válida")
        else:
            print("❌ Programación FIN DE MES NO es válida")
        
        # Probar descripción
        descripcion = programacion_fin_mes.obtener_descripcion_programacion()
        print(f"📝 Descripción: {descripcion}")
        
        print("\n" + "="*50)
        
        # Crear programación mensual combinada (días específicos + fin de mes)
        programacion_combinada = Programacion(
            id=None,
            control_id=1,
            nombre="Test Combinada",
            descripcion="Días específicos + fin de mes",
            tipo_programacion=TipoProgramacion.MENSUAL,
            activo=True,
            hora_ejecucion=time(14, 30),
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            dias_semana=None,
            dias_mes=[1, 15, -1],  # Día 1, 15 y fin de mes
            intervalo_minutos=None,
            ultima_ejecucion=None,
            proxima_ejecucion=None,
            total_ejecuciones=0,
            fecha_creacion=datetime.now(),
            fecha_modificacion=None,
            creado_por="test"
        )
        
        print(f"✅ Programación creada: {programacion_combinada.nombre}")
        print(f"   Días del mes: {programacion_combinada.dias_mes}")
        
        # Verificar validación
        if programacion_combinada.es_valida():
            print("✅ Programación COMBINADA es válida")
        else:
            print("❌ Programación COMBINADA NO es válida")
        
        # Probar descripción
        descripcion = programacion_combinada.obtener_descripcion_programacion()
        print(f"📝 Descripción: {descripcion}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_validacion_fin_de_mes()