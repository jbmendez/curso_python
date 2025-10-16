# Sistema de Notificaciones por Archivos para Motor de Controles

## Descripción General

El sistema de notificaciones proporciona capacidades completas para notificar eventos del motor de controles de manera local y remota a través de archivos compartidos. Utiliza la biblioteca `plyer` para notificaciones locales y un sistema de archivos JSON para notificaciones remotas entre equipos de la red.

## Arquitectura del Sistema

### Flujo Principal
1. **Control se dispara** → Genera Excel + archivo de notificación JSON en carpeta compartida
2. **Monitor en otros equipos** → Lee archivos de notificación → Muestra notificación local → Elimina archivo
3. **Sin dependencias de red complejas** → Solo carpetas compartidas (más estable que `msg` command)

### Ventajas de este Enfoque
- ✅ **Más confiable**: Funciona aunque los equipos estén en diferentes redes
- ✅ **Asíncrono**: No bloquea el motor si hay problemas de red
- ✅ **Auditable**: Los archivos JSON contienen toda la información del evento
- ✅ **Escalable**: Múltiples equipos pueden monitorear las mismas carpetas
- ✅ **Persistente**: Las notificaciones se procesan aunque el equipo destino esté offline

## Características Principales

### ✅ Notificaciones Locales
- Notificaciones de escritorio de Windows nativas
- Soporte para títulos y mensajes personalizados
- Límites de caracteres automáticos (60 chars título, 200 chars mensaje)
- Iconos emoji para diferentes tipos de eventos
- Timeouts configurables según tipo de evento

### ✅ Notificaciones por Archivos
- Archivos JSON depositados en carpetas compartidas junto con Excel
- Procesamiento automático por monitores en otros equipos
- Información completa del evento (origen, timestamp, datos)
- Eliminación automática después del procesamiento

### ✅ Manejo de Límites de Caracteres
- Truncamiento automático de textos largos
- Preservación de información esencial
- Métodos específicos para nombres de controles y mensajes

## Estructura de Archivos

```
src/infrastructure/services/
├── notification_service.py              # Servicio principal de notificaciones locales
├── notification_file_service.py         # Servicio para crear archivos de notificación JSON

config/
├── config_monitor_notificaciones.json   # Configuración de carpetas monitoreadas

scripts/
├── monitor_notificaciones.py            # Monitor de archivos de notificación
├── start_monitor_notificaciones.bat     # Script para ejecutar el monitor
├── test_sistema_notificaciones_archivos.py # Tests completos del sistema

ejemplos/
├── ejemplo_notificaciones_remotas.py    # Ejemplos de uso (DEPRECADO)
```

## Configuración

### Notificaciones Locales
Las notificaciones locales funcionan automáticamente si la biblioteca `plyer` está instalada:

```bash
pip install plyer==2.1.0
```

### Sistema de Archivos de Notificación

#### 1. Configurar Carpetas Compartidas
Edita `config_monitor_notificaciones.json`:

```json
{
  "carpetas_monitoreadas": [
    "C:\\temp\\reportes_test",
    "\\\\servidor\\carpeta_compartida\\notificaciones",
    "Z:\\unidad_mapeada\\reportes"
  ],
  "configuracion": {
    "intervalo_segundos": 5,
    "mantener_logs_dias": 7,
    "timeout_notificaciones": 8
  }
}
```

#### 2. Configurar Referentes con Archivos
En el sistema de controles, configura referentes que generen archivos:

```sql
-- Ejemplo de referente configurado para generar archivos y notificaciones
INSERT INTO referentes (nombre, path_archivos, notificar_por_archivo) 
VALUES ('Equipo Administración', 'C:\temp\reportes_test', 1);
```

## Uso del Sistema

### Integración Automática en el Motor
El sistema está integrado automáticamente en `EjecucionControlService`. Cuando un control se dispara y hay referentes configurados para generar archivos, se crean automáticamente:

1. **Archivo Excel** con los datos del control
2. **Archivo de notificación JSON** con metadatos del evento

```python
# En EjecucionControlService._generar_archivos_excel()
archivo_notificacion = self._notification_file_service.crear_archivo_notificacion_control(
    carpeta_destino=referente.path_archivos,
    control_nombre=control.nombre,
    filas_procesadas=sum(len(cr.get('datos', [])) for cr in consultas_resultados),
    tiempo_ejecucion_ms=resultado_ejecucion.tiempo_ejecucion_ms,
    archivo_excel=os.path.basename(archivo_generado)
)
```

### Ejecución del Monitor
En los equipos que deben recibir notificaciones:

#### Opción 1: Script BAT (recomendado)
```cmd
start_monitor_notificaciones.bat
```

#### Opción 2: Línea de comandos
```cmd
python monitor_notificaciones.py --config config_monitor_notificaciones.json
```

#### Opción 3: Con parámetros específicos
```cmd
# Solo verificar carpetas
python monitor_notificaciones.py --verificar-carpetas

# Procesar archivo específico (testing)
python monitor_notificaciones.py --test-archivo "archivo.json"

# Intervalo personalizado
python monitor_notificaciones.py --intervalo 10
```

### Formato de Archivos JSON

Los archivos de notificación siguen este formato:

```json
{
  "tipo": "control_disparado",
  "timestamp": "2024-10-16T11:42:44.486000",
  "control": {
    "nombre": "Control Mensual de Facturación",
    "filas_procesadas": 234,
    "tiempo_ejecucion_ms": 3500.0
  },
  "archivos": {
    "excel": "Control_Mensual_Facturacion_20241016_114244.xlsx"
  },
  "mensaje": {
    "titulo": "🔥 Control Disparado: Control Mensual de Facturación",
    "cuerpo": "Se ha disparado el control: Control Mensual de Facturación\nFilas procesadas: 234\nTiempo de ejecución: 3.5s"
  },
  "sistema": {
    "equipo_origen": "SERVIDOR-PRINCIPAL",
    "usuario_origen": "motor_user"
  }
}
```

## Métodos Disponibles

### NotificationFileService

#### `crear_archivo_notificacion_control(carpeta_destino, control_nombre, filas_procesadas, tiempo_ejecucion_ms, archivo_excel=None, mensaje_adicional=None)`
Crea un archivo de notificación cuando un control se dispara exitosamente.

#### `crear_archivo_notificacion_error(carpeta_destino, control_nombre, error_mensaje, tiempo_ejecucion_ms=None)`
Crea un archivo de notificación cuando un control falla.

#### `crear_archivo_notificacion_motor(carpeta_destino, tipo_evento, razon=None)`
Crea un archivo de notificación para eventos del motor (iniciado, detenido, parado).

#### `listar_archivos_notificacion(carpeta_origen)`
Lista todos los archivos de notificación en una carpeta.

#### `leer_archivo_notificacion(ruta_archivo)`
Lee y parsea un archivo de notificación JSON.

#### `eliminar_archivo_notificacion(ruta_archivo)`
Elimina un archivo de notificación después de procesarlo.

### NotificationFileMonitor

#### `iniciar_monitoreo()`
Inicia el monitoreo continuo de las carpetas configuradas.

#### `verificar_carpetas()`
Verifica que las carpetas monitoreadas existan y sean accesibles.

#### `procesar_archivo_unico(ruta_archivo)`
Procesa un archivo de notificación específico (para testing).

### WindowsNotificationService (sin cambios)

#### `mostrar_motor_iniciado()`
Muestra notificación cuando el motor se inicia.

#### `mostrar_motor_detenido()`
Muestra notificación cuando el motor se detiene normalmente.

#### `mostrar_motor_parado(razon: str)`
Muestra notificación cuando el motor se para por una razón específica.

#### `mostrar_control_disparado(control_nombre, filas_procesadas, tiempo_ejecucion_ms, mensaje_adicional=None)`
Muestra notificación cuando un control se dispara exitosamente.

#### `mostrar_control_error(control_nombre, error_mensaje, tiempo_ejecucion_ms=None)`
Muestra notificación cuando un control falla.

#### `mostrar_resumen_ejecucion(total_controles, controles_disparados, controles_error, tiempo_total_ms)`
Muestra resumen de la ejecución de controles.

## Testing y Validación

### Tests Automatizados

#### Test Completo del Sistema
```cmd
python test_sistema_notificaciones_archivos.py --test completo
```
Prueba el flujo completo: crear archivo → procesar → mostrar notificación → eliminar archivo.

#### Test de Múltiples Tipos
```cmd
python test_sistema_notificaciones_archivos.py --test tipos
```
Prueba todos los tipos de notificación (control disparado, error, motor iniciado/parado).

#### Generar Archivos de Prueba
```cmd
python test_sistema_notificaciones_archivos.py --test generar
```
Genera archivos de ejemplo en la carpeta configurada.

#### Monitor en Modo Desarrollo
```cmd
python test_sistema_notificaciones_archivos.py --test monitor
```
Ejecuta el monitor de manera continua para testing manual.

### Verificación de Funcionamiento

1. **Verificar carpetas**:
   ```cmd
   python monitor_notificaciones.py --verificar-carpetas
   ```

2. **Generar archivos de prueba**:
   ```cmd
   python test_sistema_notificaciones_archivos.py --test generar
   ```

3. **Procesar archivos manualmente**:
   ```cmd
   python monitor_notificaciones.py --test-archivo "ruta_archivo.json"
   ```

4. **Monitoreo continuo**:
   ```cmd
   start_monitor_notificaciones.bat
   ```

## Configuración de Red

### Carpetas Compartidas Recomendadas

#### Opción 1: Servidor Central
```
\\servidor-principal\notificaciones\
├── reportes_motor\      # Archivos Excel
└── notificaciones\      # Archivos JSON
```

#### Opción 2: Unidad Mapeada
```
Z:\reportes_sistema\
├── excel\              # Archivos Excel  
└── notificaciones\     # Archivos JSON
```

#### Opción 3: Múltiples Carpetas por Equipo
```
\\servidor\notificaciones\
├── equipo_admin\       # Notificaciones para administrador
├── equipo_finanzas\    # Notificaciones para finanzas
└── equipo_sistemas\    # Notificaciones para sistemas
```

### Permisos Requeridos

- **Equipo que ejecuta motor**: Escritura en carpetas compartidas
- **Equipos que reciben notificaciones**: Lectura y eliminación en carpetas monitoreadas

## Límites y Consideraciones

### Límites de Caracteres (sin cambios)
- **Títulos locales**: Máximo 60 caracteres (se truncan automáticamente)
- **Mensajes locales**: Máximo 200 caracteres
- **Nombres de controles**: Se truncan a 40 caracteres para títulos
- **Mensajes de error**: Se truncan a 100-200 caracteres según contexto

### Requisitos del Sistema
1. **Python 3.7+** con biblioteca `plyer`
2. **Carpetas compartidas** accesibles desde todos los equipos
3. **Permisos de lectura/escritura** en carpetas monitoreadas
4. **Espacio en disco** suficiente para archivos temporales

### Consideraciones de Red
- Los archivos JSON son pequeños (~1-2 KB cada uno)
- El monitor verifica carpetas cada 5 segundos por defecto (configurable)
- Los archivos se eliminan inmediatamente después del procesamiento
- Funciona con cualquier tipo de red (LAN, WAN, VPN)

### Ventajas vs Sistema MSG (anterior)
- ✅ **Más confiable**: No depende de servicios específicos de Windows
- ✅ **Funciona entre redes**: No limitado a mismo dominio/subnet
- ✅ **Asíncrono**: No bloquea el motor por problemas de red
- ✅ **Auditable**: Archivos JSON contienen información completa
- ✅ **Escalable**: Múltiples monitores pueden procesar mismos archivos
- ✅ **Sin configuración compleja**: Solo necesita carpetas compartidas

## Ejemplo Completo de Flujo

### 1. Control se Dispara en Servidor Principal
```
SERVIDOR-PRINCIPAL ejecuta control "Facturación Mensual"
↓
Genera: \\servidor\reportes\Facturacion_Mensual_20241016_114244.xlsx
Genera: \\servidor\reportes\notif_control_20241016_114244_486.json
```

### 2. Monitor en Equipo de Administración
```
EQUIPO-ADMIN ejecuta monitor_notificaciones.py
↓
Lee: \\servidor\reportes\notif_control_20241016_114244_486.json
↓
Muestra notificación local: "🔥 Control Disparado: Facturación Mensual"
↓
Elimina: notif_control_20241016_114244_486.json
```

### 3. Monitor en Equipo de Finanzas
```
EQUIPO-FINANZAS ejecuta monitor_notificaciones.py
↓
Lee: \\servidor\reportes\notif_control_20241016_114244_486.json (ya eliminado)
↓
No encuentra archivo (ya procesado por EQUIPO-ADMIN)
```

**Nota**: Para notificar múltiples equipos, configura carpetas separadas o copia archivos a múltiples ubicaciones.

## Troubleshooting

### Problema: "ImportError: cannot import name 'WindowsNotificationService'"
**Solución**: Usa `WindowsNotificationService` en lugar de `NotificationService`

### Problema: "missing required positional argument 'filas_procesadas'"
**Solución**: Incluye el parámetro `filas_procesadas` en llamadas a `mostrar_control_disparado()`

### Problema: Monitor no encuentra archivos
**Soluciones**:
1. Verifica permisos de lectura en carpetas monitoreadas
2. Confirma que la ruta de carpeta es correcta
3. Ejecuta `python monitor_notificaciones.py --verificar-carpetas`

### Problema: Monitor no puede eliminar archivos
**Soluciones**:
1. Verifica permisos de escritura/eliminación
2. Asegúrate de que los archivos no estén siendo usados por otro proceso
3. Verifica que la carpeta no esté protegida contra escritura

### Problema: Notificaciones no aparecen
**Soluciones**:
1. Verifica que plyer esté instalado: `pip install plyer`
2. Comprueba que las notificaciones de Windows estén habilitadas
3. Ejecuta test manual: `python test_sistema_notificaciones_archivos.py --test completo`

### Problema: Error de codificación en logs
**Solución**: Los emojis en logs pueden causar problemas. Los mensajes son solo informativos.

### Problema: Múltiples monitores procesan el mismo archivo
**Solución**: 
- Usa carpetas separadas para cada equipo de destino
- O configura solo un monitor por carpeta compartida

## Migración desde Sistema MSG

Si migras del sistema anterior basado en comando `msg`:

1. **Eliminar configuración antigua**:
   - Borrar `config/notificaciones_config.py`
   - Remover imports de notificaciones remotas

2. **Configurar nuevo sistema**:
   - Editar `config_monitor_notificaciones.json`
   - Configurar referentes con `notificar_por_archivo = 1`
   - Ejecutar monitores en equipos de destino

3. **Validar funcionamiento**:
   ```cmd
   python test_sistema_notificaciones_archivos.py --test completo
   ```

## Integración con Motor Existente

El sistema está completamente integrado con el motor de ejecución existente. Las notificaciones se activan automáticamente cuando:

1. El motor se inicia o se detiene (solo locales)
2. Un control se dispara exitosamente (local + archivo si hay referente configurado)
3. Un control genera un error (local + archivo si hay referente configurado)
4. Se completa un ciclo de ejecución (solo local)

Para habilitar notificaciones por archivos:
1. Configura referentes con `notificar_por_archivo = 1`
2. Especifica `path_archivos` en el referente
3. Ejecuta monitores en equipos que deben recibir notificaciones

## Logs y Depuración

### Logs del Motor (sin cambios)
```
2024-01-15 10:30:15 - INFO - Notificación local mostrada para control: Control de Facturación
2024-01-15 10:30:16 - INFO - Archivo de notificación generado: notif_control_20241015_103015_123.json
```

### Logs del Monitor
```
2024-01-15 10:30:20 - INFO - Procesando archivo: notif_control_20241015_103015_123.json
2024-01-15 10:30:21 - INFO - Archivo procesado y eliminado: notif_control_20241015_103015_123.json
2024-01-15 10:30:22 - INFO - Ciclo completado: 1/1 archivos procesados
```

Los logs ayudan a diagnosticar problemas de procesamiento y verificar el funcionamiento del sistema.

---

## Resumen de Cambios

**NUEVA ARQUITECTURA (Actual)**:
- ✅ Motor genera archivos JSON + Excel en carpetas compartidas
- ✅ Monitores en otros equipos procesan archivos y muestran notificaciones locales
- ✅ Sistema más confiable y escalable

**ARQUITECTURA ANTERIOR (Descontinuada)**:
- ❌ Motor intentaba enviar notificaciones directamente con comando `msg`
- ❌ Dependía de configuración de red específica y servicios Windows
- ❌ No funcionaba entre redes diferentes o con políticas restrictivas

El nuevo sistema es más robusto y funciona en cualquier entorno con carpetas compartidas.