#!/usr/bin/env python3
"""
Script para limpiar historial de la base de datos
"""
import sqlite3
from datetime import datetime, timedelta

def limpiar_historial():
    """Limpia el historial de ejecuciones"""
    try:
        conn = sqlite3.connect('sistema_controles.db')
        cursor = conn.cursor()
        
        # Contar registros antes
        cursor.execute("SELECT COUNT(*) FROM resultados_ejecucion")
        total_antes = cursor.fetchone()[0]
        
        print(f"📊 Registros de historial antes: {total_antes}")
        
        if total_antes == 0:
            print("✅ No hay registros para borrar")
            return
        
        # Opciones de limpieza
        print("\n🧹 Opciones de limpieza:")
        print("1. Borrar TODO el historial")
        print("2. Borrar registros anteriores a 7 días")
        print("3. Borrar registros anteriores a 30 días")
        print("4. Cancelar")
        
        opcion = input("\nSeleccione opción (1-4): ").strip()
        
        if opcion == "1":
            cursor.execute("DELETE FROM resultados_ejecucion")
            mensaje = "TODO el historial"
            
        elif opcion == "2":
            fecha_limite = datetime.now() - timedelta(days=7)
            cursor.execute("DELETE FROM resultados_ejecucion WHERE fecha_ejecucion < ?", 
                         (fecha_limite.isoformat(),))
            mensaje = "registros anteriores a 7 días"
            
        elif opcion == "3":
            fecha_limite = datetime.now() - timedelta(days=30)
            cursor.execute("DELETE FROM resultados_ejecucion WHERE fecha_ejecucion < ?", 
                         (fecha_limite.isoformat(),))
            mensaje = "registros anteriores a 30 días"
            
        elif opcion == "4":
            print("❌ Operación cancelada")
            return
            
        else:
            print("❌ Opción inválida")
            return
        
        # Confirmar cambios
        registros_eliminados = cursor.rowcount
        conn.commit()
        
        # Contar registros después
        cursor.execute("SELECT COUNT(*) FROM resultados_ejecucion")
        total_despues = cursor.fetchone()[0]
        
        print(f"✅ Eliminados {registros_eliminados} registros ({mensaje})")
        print(f"📊 Registros restantes: {total_despues}")
        
        # Optimizar base de datos
        cursor.execute("VACUUM")
        conn.commit()
        print("🔧 Base de datos optimizada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def mostrar_estadisticas():
    """Muestra estadísticas del historial"""
    try:
        conn = sqlite3.connect('sistema_controles.db')
        cursor = conn.cursor()
        
        # Total de registros
        cursor.execute("SELECT COUNT(*) FROM resultados_ejecucion")
        total = cursor.fetchone()[0]
        
        print(f"📊 Total de registros: {total}")
        
        if total > 0:
            # Fecha más antigua
            cursor.execute("SELECT MIN(fecha_ejecucion) FROM resultados_ejecucion")
            fecha_antigua = cursor.fetchone()[0]
            
            # Fecha más reciente
            cursor.execute("SELECT MAX(fecha_ejecucion) FROM resultados_ejecucion")
            fecha_reciente = cursor.fetchone()[0]
            
            print(f"📅 Registro más antiguo: {fecha_antigua}")
            print(f"📅 Registro más reciente: {fecha_reciente}")
            
            # Por estado
            cursor.execute("""
                SELECT estado, COUNT(*) 
                FROM resultados_ejecucion 
                GROUP BY estado 
                ORDER BY COUNT(*) DESC
            """)
            
            print("\n📈 Por estado:")
            for estado, cantidad in cursor.fetchall():
                print(f"   {estado}: {cantidad}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🗄️ GESTOR DE HISTORIAL DE EJECUCIONES")
    print("=" * 40)
    
    # Mostrar estadísticas primero
    mostrar_estadisticas()
    print()
    
    # Preguntar si quiere limpiar
    respuesta = input("¿Desea limpiar el historial? (s/n): ").strip().lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        limpiar_historial()
    else:
        print("✅ Operación cancelada")