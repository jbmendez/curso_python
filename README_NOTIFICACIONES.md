# 🔔 Sistema de Notificaciones por Archivos - Guía Rápida

## ¿Qué es este sistema?

Un sistema de notificaciones **confiable y escalable** que permite que el motor de controles notifique eventos a otros equipos de la red usando archivos JSON en carpetas compartidas.

## 🚀 Inicio Rápido

### 1. Configurar Carpetas Compartidas
```json
// Editar: config_monitor_notificaciones.json
{
  "carpetas_monitoreadas": [
    "C:\\temp\\reportes_test",
    "\\\\servidor\\notificaciones"
  ]
}
```

### 2. Configurar Referente (en el motor)
```sql
INSERT INTO referentes (nombre, path_archivos, notificar_por_archivo) 
VALUES ('Equipo Admin', 'C:\temp\reportes_test', 1);
```

### 3. Ejecutar Monitor (en equipos de destino)
```cmd
start_monitor_notificaciones.bat
```

### 4. Probar Sistema
```cmd
python test_sistema_notificaciones_archivos.py --test completo
```

## 📋 Flujo del Sistema

```
Control se dispara en SERVIDOR-A
↓
Genera Excel + JSON en carpeta compartida
↓
Monitor en EQUIPO-B detecta archivo JSON
↓
Muestra notificación local en EQUIPO-B
↓
Elimina archivo JSON (procesado)
```

## 🛠️ Comandos Útiles

### Testing
```cmd
# Test completo del sistema
python test_sistema_notificaciones_archivos.py --test completo

# Generar archivos de prueba
python test_sistema_notificaciones_archivos.py --test generar

# Probar múltiples tipos
python test_sistema_notificaciones_archivos.py --test tipos
```

### Monitor
```cmd
# Verificar carpetas configuradas
python monitor_notificaciones.py --verificar-carpetas

# Procesar archivo específico
python monitor_notificaciones.py --test-archivo "archivo.json"

# Monitor con intervalo personalizado
python monitor_notificaciones.py --intervalo 10
```

## 📁 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `monitor_notificaciones.py` | Monitor principal de archivos |
| `start_monitor_notificaciones.bat` | Script para ejecutar monitor |
| `config_monitor_notificaciones.json` | Configuración de carpetas |
| `test_sistema_notificaciones_archivos.py` | Tests del sistema |
| `notification_file_service.py` | Servicio para crear archivos JSON |

## 🔧 Solución de Problemas

### ❌ Monitor no encuentra archivos
- Verificar permisos de lectura en carpetas
- Confirmar rutas en configuración
- Ejecutar `--verificar-carpetas`

### ❌ No aparecen notificaciones
- Instalar: `pip install plyer`
- Verificar notificaciones Windows habilitadas
- Ejecutar test: `--test completo`

### ❌ Error al eliminar archivos
- Verificar permisos de escritura
- Comprobar que archivo no esté en uso

## ✅ Ventajas vs Sistema Anterior

| Característica | Sistema MSG (Anterior) | Sistema Archivos (Actual) |
|----------------|------------------------|---------------------------|
| **Confiabilidad** | ❌ Depende servicios Windows | ✅ Solo carpetas compartidas |
| **Entre redes** | ❌ Limitado a mismo dominio | ✅ Cualquier red con acceso |
| **Configuración** | ❌ Compleja (usuarios, IPs) | ✅ Simple (solo carpetas) |
| **Asíncrono** | ❌ Bloquea si hay problemas | ✅ No bloquea motor |
| **Auditable** | ❌ Sin rastro de mensajes | ✅ Archivos JSON completos |
| **Escalable** | ❌ Uno a uno | ✅ Múltiples monitores |

## 🏗️ Arquitectura

```
MOTOR (Servidor Principal)
├── Ejecuta controles
├── Genera Excel
└── Crea JSON notificación
         ↓
CARPETA COMPARTIDA
├── archivo.xlsx
└── notif_*.json
         ↓
MONITORES (Equipos remotos)
├── Detectan JSON
├── Muestran notificación
└── Eliminan archivo
```

## 📞 Soporte

- **Documentación completa**: `SISTEMA_NOTIFICACIONES.md`
- **Tests integrados**: `test_sistema_notificaciones_archivos.py`
- **Logs detallados**: `monitor_notificaciones.log`

---

**💡 Tip**: Para notificar múltiples equipos, usa carpetas separadas o configura múltiples monitores en diferentes ubicaciones de red.