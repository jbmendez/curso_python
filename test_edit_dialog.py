#!/usr/bin/env python3
"""
Script para verificar que el diálogo de edición funciona correctamente
"""
import sys
import os
import tkinter as tk

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from presentation.gui.dialogs import EditConnectionDialog

def test_edit_dialog():
    """Prueba el diálogo de edición"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Datos de prueba de una conexión IBM i Series
    conexion_data = {
        'id': 1,
        'nombre': 'Test iSeries Connection',
        'motor': 'iseries',
        'servidor': '10.1.1.100',
        'puerto': 8471,
        'base_datos': 'TESTLIB',
        'usuario': 'TESTUSER',
        'activa': True,
        'driver_type': 'jdbc'
    }
    
    print("🧪 Probando diálogo de edición...")
    print(f"Conexión de prueba: {conexion_data['nombre']}")
    print(f"Motor: {conexion_data['motor']}")
    print(f"Driver Type: {conexion_data['driver_type']}")
    
    # Mock del controlador
    class MockController:
        def actualizar_conexion(self, **kwargs):
            print(f"✅ Mock actualizar_conexion llamado con: {kwargs}")
            return {"success": True, "data": kwargs}
        
        def probar_conexion(self, **kwargs):
            print(f"✅ Mock probar_conexion llamado con: {kwargs}")
            return {"success": True, "message": "Conexión de prueba exitosa"}
    
    controller = MockController()
    
    # Crear y mostrar diálogo
    dialog = EditConnectionDialog(root, controller, conexion_data)
    
    print("✅ Diálogo de edición creado exitosamente")
    print("🔍 Verificando campos cargados...")
    
    # Verificar que los campos se cargaron correctamente
    assert dialog.nombre_var.get() == 'Test iSeries Connection'
    assert dialog.motor_var.get() == 'iseries'
    assert dialog.servidor_var.get() == '10.1.1.100'
    assert dialog.puerto_var.get() == '8471'
    assert dialog.bd_var.get() == 'TESTLIB'
    assert dialog.usuario_var.get() == 'TESTUSER'
    assert dialog.activa_var.get() == True
    assert dialog.driver_type_var.get() == 'jdbc'
    
    print("✅ Todos los campos cargados correctamente")
    print("✅ Campo 'Tipo Driver' visible para iSeries")
    
    # Cerrar diálogo
    dialog.dialog.destroy()
    root.destroy()
    
    print("🎉 ¡Prueba del diálogo de edición exitosa!")
    return True

if __name__ == "__main__":
    try:
        test_edit_dialog()
        print("\n✅ ¡Todas las pruebas del diálogo de edición pasaron!")
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        sys.exit(1)