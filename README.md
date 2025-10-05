# Curso Python de Vicky

Este repositorio contiene un ejemplo completo de **Clean Architecture** implementado en Python para fines educativos, incluyendo un sistema de controles SQL empresarial.

## 🏗️ Estructura del Proyecto (Clean Architecture)

```
src/
├── domain/                     # Capa de Dominio
│   ├── entities/              # Entidades de negocio
│   │   ├── usuario.py         # Entidad Usuario
│   │   ├── control.py         # Entidad Control SQL
│   │   ├── parametro.py       # Entidad Parámetro
│   │   ├── consulta.py        # Entidad Consulta SQL
│   │   ├── conexion.py        # Entidad Conexión BD
│   │   └── referente.py       # Entidad Referente
│   ├── repositories/          # Interfaces de repositorios
│   │   ├── usuario_repository.py
│   │   ├── control_repository.py
│   │   ├── parametro_repository.py
│   │   ├── consulta_repository.py
│   │   ├── conexion_repository.py
│   │   └── referente_repository.py
│   └── services/              # Servicios de dominio
│       ├── usuario_service.py
│       └── control_service.py
├── application/               # Capa de Aplicación
│   ├── use_cases/            # Casos de uso
│   │   ├── registrar_usuario_use_case.py
│   │   ├── crear_control_use_case.py
│   │   ├── crear_parametro_use_case.py
│   │   ├── crear_consulta_use_case.py
│   │   └── listar_controles_use_case.py
│   └── dto/                  # Data Transfer Objects
│       ├── usuario_dto.py
│       ├── control_dto.py
│       └── entidades_dto.py
├── infrastructure/           # Capa de Infraestructura
│   ├── database/            # Configuración de BD
│   ├── repositories/        # Implementaciones concretas
│   │   ├── sqlite_usuario_repository.py
│   │   └── sqlite_control_repository.py
│   └── external_services/   # Servicios externos
└── presentation/            # Capa de Presentación
    ├── api/                # Configuración de API
    └── controllers/        # Controladores
        ├── usuario_controller.py
        └── control_controller.py
```

## 📚 Capas de Clean Architecture

### 1. **Domain (Dominio)**
- **Entidades**: Objetos de negocio principales (`Usuario`, `Control`, `Parámetro`, etc.)
- **Repositorios**: Interfaces para acceso a datos
- **Servicios**: Lógica de negocio compleja

### 2. **Application (Aplicación)**
- **Use Cases**: Casos de uso específicos (`RegistrarUsuario`, `CrearControl`)
- **DTOs**: Objetos para transferir datos entre capas

### 3. **Infrastructure (Infraestructura)**
- **Repositorios**: Implementaciones concretas (SQLite, PostgreSQL, etc.)
- **Base de datos**: Configuraciones y migraciones
- **Servicios externos**: APIs, email, etc.

### 4. **Presentation (Presentación)**
- **Controladores**: Manejo de peticiones HTTP
- **APIs**: Endpoints REST
- **Interfaces**: UI, CLI, etc.

## 🎯 Sistema de Controles SQL

### Funcionalidades Principales:
- **Gestión de Controles**: Crear y administrar controles SQL
- **Parámetros Dinámicos**: Definir parámetros tipados para consultas
- **Consultas SQL**: Gestionar consultas de disparo y validación
- **Conexiones BD**: Configurar conexiones a diferentes bases de datos
- **Referentes**: Gestionar notificaciones por email y archivo
- **Ejecución Automatizada**: Sistema para ejecutar controles y reportar resultados

### Entidades del Sistema:
- **Control**: Configuración principal del control con consultas y parámetros
- **Parámetro**: Parámetros tipados (string, integer, date, etc.)
- **Consulta**: Consultas SQL con validaciones de seguridad
- **Conexión**: Configuración de conexiones a bases de datos
- **Referente**: Usuarios para notificaciones (email, archivos)

## 🚀 Cómo ejecutar

```bash
# Ejecutar ejemplo básico de usuarios
python main.py

# Ejecutar ejemplo del sistema de controles
python ejemplo_controles.py

# Ejecutar tests
python -m pytest tests/ -v

# Ejecutar test específico
python -m pytest tests/unit/test_usuario.py -v
python -m pytest tests/unit/test_control.py -v
```

## 💡 Conceptos Clave

- **Inversión de dependencias**: Las capas internas no dependen de las externas
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Testabilidad**: Cada capa se puede testear independientemente
- **Mantenibilidad**: Código organizado y fácil de modificar
- **Validaciones de Dominio**: Reglas de negocio en las entidades
- **Repositorio Pattern**: Abstracción del acceso a datos

## � Próximos Desarrollos

- [ ] Implementar repositorios SQLite para todas las entidades
- [ ] Sistema de ejecución de controles SQL
- [ ] Servicio de notificaciones (email, archivos)
- [ ] API REST completa con FastAPI
- [ ] Sistema de logs y auditoria
- [ ] Dashboard web para gestión

## �📖 Recursos para Aprender

- [Clean Architecture por Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
