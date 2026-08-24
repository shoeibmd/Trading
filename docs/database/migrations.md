# Migration Guide

Migrations are managed with Alembic.

## Commands
- **Generate Migration**: `alembic revision --autogenerate -m "Message"`
- **Apply Migration**: `alembic upgrade head`
- **Rollback Migration**: `alembic downgrade -1`

## Offline SQL Generation
Generate SQL for DBA review without executing:
`alembic upgrade head --sql`
