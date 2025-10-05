#!/usr/bin/env python3
"""
Script principal simplificado para la aplicación de escritorio
Compatible con versiones anteriores de macOS
"""

import sys
import os

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_compatibility():
    """Verifica compatibilidad del sistema"""
    try:
        import tkinter as tk
        # Crear una ventana básica para verificar que funciona
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Error de Tkinter: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando Sistema de Gestión de Controles SQL...")
    print("📋 Interfaz: Tkinter Desktop (Compatible)")
    print("🏗️  Arquitectura: Clean Architecture")
    print("💾 Base de datos: SQLite")
    print("-" * 50)
    
    # Verificar compatibilidad antes de importar la aplicación principal
    if not check_compatibility():
        print("❌ Tkinter no está funcionando correctamente")
        print("💡 Sugerencias:")
        print("   - Instala Python desde python.org (incluye Tkinter)")
        print("   - Verifica que macOS sea compatible")
        print("   - Usa: brew install python-tk")
        return 1
    
    try:
        # Importar solo después de verificar compatibilidad
        from infrastructure.database.database_setup import DatabaseSetup
        
        # Configurar base de datos
        print("📦 Configurando base de datos...")
        db_setup = DatabaseSetup()
        db_setup.initialize_database()
        print("✅ Base de datos configurada")
        
        # Intentar importar la aplicación principal
        try:
            from presentation.gui.main_window import MainWindow
            app = MainWindow()
            print("🎨 Iniciando interfaz gráfica...")
            app.run()
        except ImportError as ie:
            print(f"❌ Error al importar la aplicación principal: {ie}")
            print("📝 Usando interfaz de línea de comandos alternativa...")
            run_cli_alternative()
            
    except KeyboardInterrupt:
        print("\n⏹️  Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1
    
    print("👋 ¡Hasta luego!")
    return 0

def run_cli_alternative():
    """Interfaz de línea de comandos alternativa"""
    print("\n" + "="*50)
    print("🖥️  INTERFAZ DE LÍNEA DE COMANDOS")
    print("="*50)
    
    while True:
        print("\n📋 Opciones disponibles:")
        print("1. 📊 Listar controles")
        print("2. 🔗 Listar conexiones")
        print("3. ⚡ Ejecutar control (simulado)")
        print("4. 📈 Ver historial")
        print("0. 🚪 Salir")
        
        try:
            opcion = input("\n🎯 Selecciona una opción: ").strip()
            
            if opcion == "0":
                break
            elif opcion == "1":
                print("📊 Función de listar controles - Por implementar")
            elif opcion == "2":
                print("🔗 Función de listar conexiones - Por implementar")
            elif opcion == "3":
                print("⚡ Función de ejecutar control - Por implementar")
            elif opcion == "4":
                print("📈 Función de ver historial - Por implementar")
            else:
                print("❌ Opción no válida")
                
        except (KeyboardInterrupt, EOFError):
            break
    
    print("\n👋 Saliendo de la interfaz de línea de comandos...")

if __name__ == "__main__":
    sys.exit(main())