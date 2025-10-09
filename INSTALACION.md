# 🚀 Instalación del Sistema de Controles

## 📋 Requisitos Previos

### 1. **Python 3.8+**
- Descargar desde: https://python.org
- ✅ Asegúrate de marcar "Add Python to PATH" durante la instalación

### 2. **Java 11 JDK** (para conexión iSeries)
- Instalar en: `C:\Program Files\Java\jdk-11`
- Descargar desde: https://adoptium.net/temurin/releases/

### 3. **jt400.jar** (driver IBM iSeries)
- Descargar desde: https://www.ibm.com/support/pages/java-toolbox-i-jtopen
- Colocar en: `drivers/jt400.jar`

## 🛠️ Instalación Automática

### Opción 1: Script de instalación (Recomendado)
```bash
# 1. Clonar repositorio
git clone https://github.com/jbmendez/curso_python.git
cd curso_python

# 2. Ejecutar instalación automática
install.bat
```

### Opción 2: Instalación manual
```bash
# 1. Clonar repositorio
git clone https://github.com/jbmendez/curso_python.git
cd curso_python

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Configurar Java (si es necesario)
set JAVA_HOME=C:\Program Files\Java\jdk-11

# 4. Inicializar base de datos
python -c "from src.infrastructure.database.database_setup import DatabaseSetup; db = DatabaseSetup(); db.initialize_database(); print('✅ DB OK')"

# 5. Crear carpeta de logs
mkdir logs
```

## 🚀 Uso del Sistema

### **GUI Principal**
```bash
# Abrir interfaz gráfica
start_gui.bat
# o directamente:
py main_gui.py
```

### **Motor de Ejecución Automática**
```bash
# Gestionar motor
py gestionar_motor.py iniciar    # Iniciar motor
py gestionar_motor.py detener    # Detener motor  
py gestionar_motor.py estado     # Ver estado

# Ejecutar motor directamente (con logs)
py motor_ejecucion.py
```

### **Verificaciones**
```bash
# Verificar base de datos
py verificar_db.py

# Listar programaciones
py test_motor.py listar

# Verificar estructura de tablas
py verificar_tablas.py
```

## 📁 Estructura del Proyecto

```
curso_python/
├── 📄 sistema_controles.db         # Base de datos SQLite
├── 📂 src/                         # Código fuente
│   ├── 📂 domain/                  # Entidades y reglas de negocio
│   ├── 📂 application/             # Casos de uso y DTOs
│   ├── 📂 infrastructure/          # Repositorios y servicios
│   └── 📂 presentation/            # GUI y controladores
├── 📂 drivers/                     # Drivers de conexión
│   └── 📄 jt400.jar               # Driver IBM iSeries
├── 📂 logs/                        # Archivos de log
├── 🛠️ motor_ejecucion.py          # Motor de ejecución automática
├── 🛠️ gestionar_motor.py          # Gestión del motor
├── 🖥️ main_gui.py                 # GUI principal
├── 🚀 start_gui.bat               # Launcher de GUI
└── 📋 requirements.txt            # Dependencias Python
```

## ⚙️ Configuración

### **Conexiones de Base de Datos**
- Configurar desde la GUI: Menú "Conexiones"
- Soporte para: iSeries, PostgreSQL, MySQL, SQL Server

### **Controles y Consultas**
- Crear desde la GUI: Menú "Controles" y "Consultas"
- Asociar consultas a controles para ejecución automática

### **Programaciones**
- Configurar desde la GUI: Menú "Programaciones"
- Tipos: Diaria, Semanal, Mensual, Intervalo, Una vez

### **Referentes y Excel**
- Configurar desde la GUI: Menú "Referentes"
- Asociar a controles para generar archivos Excel automáticamente

## 🔧 Solución de Problemas

### Error "numpy not found"
```bash
# Usar Python del sistema en lugar del virtual env
deactivate  # Si estás en .venv
py main_gui.py
```

### Error de conexión Java/iSeries
```bash
# Verificar Java 11
java -version

# Verificar JAVA_HOME
echo %JAVA_HOME%

# Verificar jt400.jar
dir drivers\jt400.jar
```

### Error de permisos SQLite
```bash
# Verificar permisos en la carpeta del proyecto
# Ejecutar como administrador si es necesario
```

## 📞 Soporte

- **Logs del motor**: `logs/motor_ejecucion_YYYYMMDD.log`
- **Logs de aplicación**: Consola durante ejecución
- **Base de datos**: SQLite Browser para inspección manual

## 🎯 Primeros Pasos

1. **Ejecutar `install.bat`** para instalación automática
2. **Abrir GUI** con `start_gui.bat`
3. **Configurar una conexión** de base de datos
4. **Crear un control** con consultas
5. **Configurar programación** automática
6. **Iniciar motor** con `py gestionar_motor.py iniciar`
7. **Verificar ejecución** en logs