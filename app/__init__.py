import logging
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.shared.bases.base_model import ModelMixin
from app import base_dir
from loguru import logger
import sentry_sdk
logger.configure(
    handlers=[
        {
            "sink": f"{base_dir}/app.log",
            "level": logging.INFO,
            "format": "{time} {level} {message}",
            "backtrace": True,
            "diagnose": True,

        }

    ]
)


sentry_sdk.init(
    traces_sample_rate=1.0,
    dsn="https://2b423e58b39c41eeb25db4c33b9203eb@o1351112.ingest.sentry.io/4505433874235392",
    max_breadcrumbs=100,
    debug=True,
    environment="development",
    release="ouroboros@0.0.1",
    send_default_pii=True,
    attach_stacktrace=True,
    request_bodies="always",
    profiles_sample_rate=1.0,


)
# create engione with postgres and psycopg2
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/ouroboros"
)
session = sessionmaker(bind=engine)
# make a scoped session
db = session()


with db:
    ModelMixin.set_session(db)

