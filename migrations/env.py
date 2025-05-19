from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config

# Alembic config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем метаданные моделей
from app.models import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using async engine."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection):
        def run_migrations(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(run_migrations)

    async def async_main():
        async with connectable.connect() as connection:
            await do_run_migrations(connection)

    asyncio.run(async_main())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
