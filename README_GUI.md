# Aplicación de Escritorio - Sistema de Gestión de Controles SQL

## 🖥️ Interfaz de Escritorio Tkinter

Esta aplicación de escritorio proporciona una interfaz gráfica completa para gestionar controles SQL en entornos bancarios restringidos.

## 🚀 Características

### ✨ Interfaz Principal
- **Pestañas organizadas**: Controles, Conexiones, Ejecución, Historial
- **Menús contextuales**: Acceso rápido a funciones principales
- **Barras de herramientas**: Iconos intuitivos para acciones comunes
- **Estado en tiempo real**: Actualización automática de datos

### 🎯 Funcionalidades

#### 📋 Gestión de Controles
- ✅ Crear nuevos controles SQL
- 👁️ Visualizar lista completa de controles
- ✏️ Editar controles existentes
- 🗑️ Eliminar controles (con confirmación)
- 🔍 Buscar y filtrar controles

#### 🔗 Gestión de Conexiones
- ✅ Crear conexiones a bases de datos
- 🏷️ Soporte para múltiples motores (MySQL, PostgreSQL, SQL Server, Oracle)
- 🧪 Probar conectividad
- ⚙️ Configurar parámetros de conexión

#### ⚡ Ejecución de Controles
- 🎮 Interfaz intuitiva para ejecutar controles
- 📊 Parámetros personalizables por control
- 🎯 Modo "solo disparo" para pruebas
- 🔄 Ejecución simulada (mock) para desarrollo
- 📈 Resultados en tiempo real

#### 📊 Historial de Ejecuciones
- 📅 Vista completa del historial
- 🔍 Filtros por control, fecha, estado
- 📋 Detalles de cada ejecución
- 📊 Métricas de rendimiento

## 🏗️ Arquitectura

### Clean Architecture Implementation
```
🎨 Presentation Layer (GUI)
├── main_window.py     # Ventana principal con pestañas
├── dialogs.py         # Ventanas de diálogo modales
└── components/        # Componentes reutilizables

🔧 Application Layer (Use Cases)
├── Controllers        # Lógica de presentación
└── Use Cases         # Casos de uso de negocio

🏪 Domain Layer (Business Logic)
├── Entities          # Entidades de dominio
├── Repositories      # Interfaces de datos
└── Services          # Servicios de dominio

🏗️ Infrastructure Layer (Data)
├── SQLite Repos     # Implementaciones concretas
├── Database Config  # Configuración de BD
└── External APIs    # Servicios externos
```

## 🚀 Ejecución

### Requisitos Previos
- **Python 3.8+** (incluye Tkinter por defecto)
- **SQLite** (incluido en Python)
- **Librerías estándar únicamente** (cumplimiento bancario)

### Lanzar la Aplicación
```bash
# Desde el directorio raíz del proyecto
python main_gui.py
```

### Primera Ejecución
1. 🏗️ La base de datos SQLite se crea automáticamente
2. 📁 Se inicializan las tablas necesarias
3. 🎯 La interfaz se abre lista para usar

## 🔧 Configuración

### Base de Datos
- **Archivo**: `data/controles.db` (se crea automáticamente)
- **Motor**: SQLite (sin servidor requerido)
- **Tablas**: usuarios, conexiones, controles, ejecuciones

### Personalización
- **Tema**: Interfaz nativa del sistema operativo
- **Tamaño**: Ventana redimensionable (1200x800 por defecto)
- **Idioma**: Español (textos y mensajes)

## 🎨 Guía de Uso

### Crear una Nueva Conexión
1. 📊 Ve a la pestaña "Conexiones"
2. ➕ Haz clic en "Nueva Conexión"
3. 📝 Completa el formulario:
   - Nombre descriptivo
   - Tipo de motor (MySQL, PostgreSQL, etc.)
   - Servidor y puerto
   - Base de datos
   - Credenciales
4. ✅ Haz clic en "Crear"

### Crear un Control SQL
1. 📋 Ve a la pestaña "Controles"
2. ➕ Haz clic en "Nuevo Control"
3. 📝 Completa el formulario:
   - Nombre del control
   - Descripción
   - Conexión asociada
   - Query SQL de disparo
   - Query SQL de acción (opcional)
4. ✅ Haz clic en "Crear"

### Ejecutar un Control
1. ⚡ Ve a la pestaña "Ejecución"
2. 🎯 Selecciona un control de la lista
3. ▶️ Haz clic en "Ejecutar Control"
4. ⚙️ Configura parámetros en el diálogo:
   - Parámetros adicionales
   - Modo de ejecución
   - Opciones avanzadas
5. 🚀 Confirma la ejecución

### Ver Historial
1. 📊 Ve a la pestaña "Historial"
2. 🔍 Usa filtros para encontrar ejecuciones específicas
3. 👁️ Haz doble clic en una fila para ver detalles

## 🏦 Entornos Bancarios

### Restricciones Cumplidas
- ✅ **Sin dependencias externas**: Solo librerías estándar de Python
- ✅ **Base de datos local**: SQLite sin servidor requerido
- ✅ **Instalación simple**: Un solo ejecutable
- ✅ **Seguridad**: Sin conexiones externas no autorizadas
- ✅ **Auditabilidad**: Logs completos de todas las operaciones

### Ventajas para Bancos
- 🔒 **Seguridad**: Interfaz local sin exposición web
- 📋 **Compliance**: Cumple regulaciones de software bancario
- 🚀 **Rendimiento**: Ejecución nativa sin navegador
- 🛠️ **Mantenimiento**: Fácil distribución e instalación
- 📊 **Monitoreo**: Historial completo de operaciones

## 🐛 Solución de Problemas

### Error: "Import could not be resolved"
```bash
# Verifica que estés en el directorio correcto
pwd
# Debe mostrar: .../curso_python

# Verifica la estructura de archivos
ls -la src/presentation/gui/
```

### La aplicación no inicia
```bash
# Verifica la versión de Python
python --version
# Debe ser 3.8 o superior

# Verifica que Tkinter esté disponible
python -c "import tkinter; print('Tkinter OK')"
```

### Base de datos no se crea
```bash
# Verifica permisos de escritura
touch data/test.db && rm data/test.db
# Si falla, revisa permisos del directorio
```

## 📚 Más Información

- 📖 **Arquitectura**: Consulta `/docs/clean-architecture.md`
- 🔧 **API**: Revisa controladores en `/src/presentation/controllers/`
- 🧪 **Testing**: Ejecuta `python -m pytest tests/`
- 📝 **Logs**: Archivos en `/logs/` (si están habilitados)

## 🤝 Contribución

Para modificar la interfaz:
1. 🔧 Edita `src/presentation/gui/main_window.py`
2. 🎨 Agrega diálogos en `src/presentation/gui/dialogs.py`
3. 🧪 Prueba con `python main_gui.py`
4. 📝 Documenta cambios en este README