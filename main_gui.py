#!/usr/bin/env python3
"""
Script principal para lanzar la aplicación de escritorio
Sistema de Gestión de Controles SQL - Clean Architecture
"""

import sys
import os

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from presentation.gui.main_window import MainWindow
    
    def main():
        """Función principal"""
        print("🚀 Iniciando Sistema de Gestión de Controles SQL...")
        print("📋 Interfaz: Tkinter Desktop")
        print("🏗️  Arquitectura: Clean Architecture")
        print("💾 Base de datos: SQLite")
        print("🏦 Optimizado para entornos bancarios")
        print("-" * 50)
        
        try:
            app = MainWindow()
            app.run()
        except KeyboardInterrupt:
            print("\n⏹️  Aplicación cerrada por el usuario")
        except Exception as e:
            print(f"❌ Error al iniciar la aplicación: {e}")
            sys.exit(1)
        
        print("👋 ¡Hasta luego!")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("📝 Verifica que la estructura del proyecto esté completa")
    print("📁 Debe existir: src/presentation/gui/main_window.py")
    sys.exit(1)