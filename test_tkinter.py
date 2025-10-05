#!/usr/bin/env python3
"""
Test básico de Tkinter para verificar compatibilidad
"""

import sys

def test_tkinter():
    """Prueba básica de Tkinter"""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        print("🧪 Creando ventana de prueba...")
        
        # Crear ventana principal
        root = tk.Tk()
        root.title("Test Tkinter - Sistema de Controles SQL")
        root.geometry("600x400")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="✅ Tkinter funcionando correctamente", 
                               style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=10)
        
        # Información del sistema
        info_text = tk.Text(main_frame, height=15, width=70)
        info_text.grid(row=1, column=0, pady=10)
        
        # Información del sistema
        import platform
        info = f"""
🖥️  Sistema Operativo: {platform.system()} {platform.release()}
🐍 Python: {sys.version}
📦 Tkinter: {tk.TkVersion}
🎨 Ttk: Disponible

🎯 NEXT STEPS:
1. Tkinter está funcionando correctamente
2. Se puede proceder con la aplicación principal
3. Compatible con Clean Architecture

🚀 Para lanzar la aplicación completa:
   python3 main_gui.py

📋 Para más información:
   Consulta README_GUI.md
"""
        
        info_text.insert("1.0", info)
        info_text.config(state="disabled")
        
        # Botón de prueba
        def show_message():
            messagebox.showinfo("Prueba", "🎉 ¡Tkinter funciona perfectamente!")
        
        test_button = ttk.Button(main_frame, text="🧪 Probar Diálogo", command=show_message)
        test_button.grid(row=2, column=0, pady=10)
        
        # Botón para cerrar
        close_button = ttk.Button(main_frame, text="🚪 Cerrar", command=root.quit)
        close_button.grid(row=3, column=0, pady=5)
        
        # Configurar grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        print("✅ Ventana creada. Iniciando bucle principal...")
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Error en test de Tkinter: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 Test de Compatibilidad Tkinter")
    print("=" * 40)
    
    if test_tkinter():
        print("✅ Test completado exitosamente")
        return 0
    else:
        print("❌ Test falló")
        return 1

if __name__ == "__main__":
    sys.exit(main())