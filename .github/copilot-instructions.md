# Clean Architecture Python Course Guidelines

## Project Overview
This is "Curso Python de Vicky" - an educational Python course repository demonstrating **Clean Architecture** patterns. The project serves as both a learning resource and a practical implementation example.

## Architecture Patterns

### Clean Architecture Structure
Follow the established 4-layer architecture:
- **Domain**: Business entities, repository interfaces, domain services (`src/domain/`)
- **Application**: Use cases, DTOs, application logic (`src/application/`)
- **Infrastructure**: Concrete implementations, databases, external services (`src/infrastructure/`)
- **Presentation**: Controllers, APIs, user interfaces (`src/presentation/`)

### Key Principles
- **Dependency Inversion**: Inner layers never depend on outer layers
- **Single Responsibility**: Each class/module has one reason to change
- **Interface Segregation**: Use abstract base classes for contracts
- **Dependency Injection**: Pass dependencies through constructors

## Development Patterns

### Entity Design
- Use `@dataclass` for entities with business logic methods
- Include validation methods within entities (`es_email_valido()`)
- Keep entities framework-agnostic and focused on business rules
- Example: `src/domain/entities/usuario.py`

### Repository Pattern
- Define abstract interfaces in `src/domain/repositories/`
- Implement concrete classes in `src/infrastructure/repositories/`
- Use type hints and return domain entities
- Follow naming: `EntityRepository` (interface) → `SQLiteEntityRepository` (implementation)

### Use Case Implementation
- One class per use case in `src/application/use_cases/`
- Accept DTOs as input, return DTOs as output
- Orchestrate domain services and repositories
- Handle application-specific validation and error handling

### DTO Usage
- Create separate DTOs for input/output in `src/application/dto/`
- Use `@dataclass` for simple data structures
- Naming pattern: `CrearEntityDTO`, `EntityResponseDTO`

## Code Organization

### File Naming Conventions
- Use Spanish names for domain concepts: `usuario.py`, `registrar_usuario_use_case.py`
- Follow snake_case for files and modules
- Use descriptive names that reflect business concepts

### Testing Strategy
- Unit tests for domain entities and services in `tests/unit/`
- Integration tests for repository implementations in `tests/integration/`
- Test each layer independently using mocks/stubs
- Use pytest for test runner with descriptive test names

### Error Handling
- Raise `ValueError` for business rule violations
- Use specific exception types in domain layer
- Handle technical errors in infrastructure layer
- Return error responses in presentation layer

## Development Workflow

### Adding New Features
1. Start with domain entities and business rules
2. Define repository interfaces if data access needed
3. Create use cases to orchestrate operations
4. Implement infrastructure (database, external services)
5. Add presentation layer (controllers, endpoints)
6. Write tests for each layer

### Database Integration
- Use repository pattern for data access abstraction
- Implement concrete repositories in `src/infrastructure/repositories/`
- Keep SQL/ORM code isolated in infrastructure layer
- Use dependency injection to swap implementations

## Key Files and Examples
- **Domain Entity**: `src/domain/entities/usuario.py` - Business object with rules
- **Repository Interface**: `src/domain/repositories/usuario_repository.py` - Data access contract
- **Use Case**: `src/application/use_cases/registrar_usuario_use_case.py` - Application logic
- **Implementation**: `src/infrastructure/repositories/sqlite_usuario_repository.py` - Concrete data access
- **Controller**: `src/presentation/controllers/usuario_controller.py` - HTTP handling
- **Integration Example**: `main.py` - Complete dependency setup and usage