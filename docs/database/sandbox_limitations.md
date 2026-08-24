# Sandbox Limitations & Validations

## Limitations
- Due to the offline nature of the sandbox environment and restricted permissions for Docker-in-Docker overlayfs, a native PostgreSQL instance running TimescaleDB was inaccessible at build time.

## What was validated:
- `alembic check` and `alembic upgrade head --sql` were successfully executed statically to ensure robust translation of SQLAlchemy models into native SQL DDL.
- `pytest` passes validating SQLAlchemy Python models parsing structure natively without requiring an engine dialer.

## To test in a full local environment:
- Make sure `docker-compose up` establishes `postgres` effectively.
- Run `alembic upgrade head` to run all migrations.
- Validate the TimescaleDB hypertable injection script runs effectively by describing `\d+ quotes` locally in PSQL.
