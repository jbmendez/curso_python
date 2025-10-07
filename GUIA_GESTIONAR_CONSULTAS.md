# 📋 Guía: Cómo Gestionar Consultas de un Control

## 🎯 Ubicación de la Funcionalidad

### Paso 1: Abrir la Aplicación
```bash
python main_gui.py
```

### Paso 2: Ir a la Pestaña "Controles"
- En la ventana principal, haz clic en la pestaña **"Controles"**

### Paso 3: Seleccionar un Control
- En la lista de controles, **haz clic en una fila** para seleccionar un control
- La fila se resaltará en azul cuando esté seleccionada

### Paso 4: Hacer Clic en "Gestionar Consultas"
- Una vez seleccionado el control, haz clic en el botón **"Gestionar Consultas"**
- Este botón está en la fila de botones superior: [Nuevo Control] [Editar Control] **[Gestionar Consultas]** [Eliminar Control] [Actualizar]

## 📋 Diálogo de Gestión de Consultas

Cuando hagas clic en "Gestionar Consultas", se abrirá una ventana con:

### Columna Izquierda: "Consultas Disponibles"
- Muestra todas las consultas que NO están asociadas al control
- Columnas: ID, Nombre, Descripción

### Columna Derecha: "Consultas Asociadas"
- Muestra las consultas YA asociadas al control
- Columnas: ID, Nombre, Orden, Es Disparo

### Botones de Acción:
1. **"→ Asociar"** - Mueve una consulta de disponible a asociada
2. **"← Desasociar"** - Mueve una consulta de asociada a disponible  
3. **"Marcar Disparo"** - Marca la consulta seleccionada como disparo
4. **"Nueva Consulta"** - Crea una nueva consulta y la asocia automáticamente

## ⚠️ Solución de Problemas

### Si no ves el botón "Gestionar Consultas":
1. Verifica que estés en la pestaña "Controles"
2. Asegúrate de que la aplicación se haya iniciado correctamente

### Si el botón está deshabilitado:
1. Primero debes **seleccionar un control** de la lista
2. Haz clic en una fila de la tabla de controles

### Si aparece un error al hacer clic:
1. Verifica que hayas seleccionado un control válido
2. Revisa la consola para ver mensajes de error detallados

## 🔧 Funcionalidad Completa

- ✅ Asociar consultas existentes a un control
- ✅ Desasociar consultas de un control
- ✅ Marcar una consulta como "disparo" (solo una por control)
- ✅ Crear nuevas consultas directamente desde el diálogo
- ✅ Ver orden de ejecución de las consultas
- ✅ Gestionar múltiples consultas por control