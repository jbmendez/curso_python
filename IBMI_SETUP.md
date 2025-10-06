# Guía de Configuración para IBM i Series (AS/400)

El sistema soporta **dos métodos** para conectar a IBM i Series:

## 🏆 Opción 1: JDBC (Recomendada)

### Ventajas:
- ✅ Más estable y confiable
- ✅ No requiere instalación de software del sistema
- ✅ Funciona en cualquier SO con Java
- ✅ Ampliamente usado en la industria

### Instalación:

1. **Instalar dependencia Python:**
   ```bash
   pip install jaydebeapi
   ```

2. **Descargar driver JT400:**
   - Ir a: https://sourceforge.net/projects/jt400/
   - Descargar: `jt400.jar` (última versión)
   - Colocar en: `drivers/jt400.jar`

3. **Verificar Java Runtime:**
   ```bash
   java -version
   ```
   Si no tienes Java, descargar de: https://www.oracle.com/java/technologies/downloads/

### Configuración en la aplicación:
- **Tipo de Motor**: Seleccionar "IBM i Series JDBC" 
- **Puerto**: 8471 (por defecto) o el configurado en tu AS/400
- **Servidor**: IP o nombre del servidor IBM i
- **Usuario/Contraseña**: Credenciales del AS/400
- **Base Datos**: Biblioteca inicial (opcional)

---

## 🔧 Opción 2: ODBC (Alternativa)

### Ventajas:
- ✅ Integración nativa con Windows
- ✅ Puede usar DSN preconfigurados

### Instalación:

1. **Instalar IBM i Access Client Solutions:**
   - Descargar desde IBM Developer o sitio oficial
   - Instalar el paquete completo
   - Configurar driver ODBC

2. **Configurar DSN (opcional):**
   - Abrir "ODBC Data Sources" en Windows
   - Crear nuevo DSN con driver IBM i Access ODBC
   - Configurar servidor, usuario, biblioteca

### Configuración en la aplicación:
- **Tipo de Motor**: Seleccionar "IBM i Series"
- **Puerto**: 446 (SSL) o 8471 (sin SSL)
- **Servidor**: IP o nombre del servidor IBM i
- **Usuario/Contraseña**: Credenciales del AS/400
- **Base Datos**: Biblioteca inicial

---

## 📊 Comparación Rápida

| Característica | JDBC | ODBC |
|---------------|------|------|
| **Instalación** | Solo jt400.jar | Software completo IBM |
| **Portabilidad** | ✅ Multiplataforma | ❌ Principalmente Windows |
| **Configuración** | ✅ Simple | ❌ Compleja |
| **Estabilidad** | ✅ Muy estable | ⚠️ Depende de versiones |
| **Rendimiento** | ✅ Excelente | ✅ Bueno |
| **Recomendado** | ✅ **SÍ** | ⚠️ Solo si ya lo tienes |

---

## 🔍 Solución de Problemas

### Error: "No se encontró el driver JDBC"
- Verificar que `jt400.jar` esté en `drivers/jt400.jar`
- Verificar que Java esté instalado
- Verificar permisos de archivo

### Error: "No se encontró driver ODBC"
- Instalar IBM i Access Client Solutions
- Verificar que el driver ODBC esté registrado
- Verificar configuración DSN

### Error: "Conexión rechazada"
- Verificar IP/nombre del servidor
- Verificar puerto (8471 vs 446)
- Verificar firewall/conectividad de red
- Verificar que el servicio esté activo en AS/400

### Error: "Credenciales inválidas"
- Verificar usuario y contraseña
- Verificar que el usuario tenga permisos en AS/400
- Verificar que el usuario no esté bloqueado

---

## 🚀 Prueba Rápida

Para verificar que todo funciona:

```bash
python test_ibmiseries_comparison.py
```

Este script probará ambas opciones y te mostrará cuál está configurada correctamente.

---

## 💡 Recomendación Final

**Usa JDBC** a menos que ya tengas ODBC configurado y funcionando. Es más simple, estable y portable.