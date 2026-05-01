"""Shared database module — provides get_db() for all blueprints."""
from flask import g, current_app
from sqlalchemy import create_engine


def get_db():
    """Return a SQLAlchemy engine, cached on Flask's g object per request."""
    if "_db_engine" not in g:
        cfg = current_app.config
        connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            cfg["DB_USER"], cfg["DB_PASSWORD"],
            cfg["DB_HOST"], cfg["DB_PORT"], cfg["DB_NAME"]
        )
        g._db_engine = create_engine(connection_string)
    return g._db_engine


def teardown_db(exception):
    engine = g.pop("_db_engine", None)
    if engine is not None:
        engine.dispose()
