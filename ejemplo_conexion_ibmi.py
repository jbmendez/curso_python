"""
Ejemplo de configuración para conexión IBM i Series.
Copia este archivo y personaliza con tus datos.
"""

# Datos de conexión de ejemplo
CONEXION_EJEMPLO = {
    "nombre": "MiIBMi",
    "tipo_motor": "ibmiseries",
    "servidor": "192.168.1.100",  # IP de tu sistema IBM i
    "puerto": 446,                # Puerto estándar para JDBC
    "base_datos": "MYLIB",        # Biblioteca inicial
    "usuario": "MIUSUARIO",       # Usuario IBM i
    "contraseña": "MIPASSWORD",   # Contraseña
    "driver_type": "odbc"         # SOLO ODBC (evita problemas de Java)
}

# Para probar desde código:
if __name__ == "__main__":
    from src.domain.entities.conexion import Conexion
    from src.infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector
    
    # Crear entidad de conexión
    conexion = Conexion(
        nombre=CONEXION_EJEMPLO["nombre"],
        tipo_motor=CONEXION_EJEMPLO["tipo_motor"],
        servidor=CONEXION_EJEMPLO["servidor"],
        puerto=CONEXION_EJEMPLO["puerto"],
        base_datos=CONEXION_EJEMPLO["base_datos"],
        usuario=CONEXION_EJEMPLO["usuario"],
        contraseña=CONEXION_EJEMPLO["contraseña"],
        driver_type=CONEXION_EJEMPLO["driver_type"]
    )
    
    # Probar conexión
    selector = IBMiSeriesConexionSelector()
    resultado = selector.probar_conexion(conexion)
    
    print(f"Resultado: {resultado.mensaje}")
    if not resultado.exitosa:
        print(f"Error: {resultado.detalles_error}")
