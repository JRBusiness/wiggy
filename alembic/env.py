import logging
import os
import sys

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

import settings


from app.shared.bases.base_model import ModelMixin as Base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)
config = context.config
url = f"postgresql+psycopg2://{settings.Config.postgres_connection}"
config.set_main_option("sqlalchemy.url", url)
alembic_config = config.get_section(config.config_ini_section)
connectable = engine_from_config(
    alembic_config, prefix="sqlalchemy.", poolclass=pool.NullPool
)

target_base = Base.metadata

with connectable.connect() as connect:
    context.configure(
        connection=connect, target_metadata=target_base, include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()
