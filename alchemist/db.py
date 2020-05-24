from typing import List

import pyodbc

from . import config

_connections = dict()


def connection(db_name="default"):
    if not _connections.get(db_name):
        db_config = config.DATABASES[db_name]

        _connections[db_name] = pyodbc.connect(
            driver=db_config.get("driver", "FreeTDS"),
            tds_version=db_config.get("tds_version", "8.0"),
            server=db_config.get("server"),
            port=db_config.get("port", 1433),
            database=db_config.get("database"),
            uid=db_config.get("user"),
            pwd=db_config.get("password"),
            autocommit=db_config.get("autocommit", False),
            timeout=db_config.get("timeout", 0),
        )

    return _connections[db_name]


def row_as_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def cursor_fetchall(cursor) -> List[dict]:
    return [row_as_dict(cursor, row) for row in cursor.fetchall()]


def cursor_fetchone(cursor) -> dict:
    row = cursor.fetchone()
    return row_as_dict(cursor, row) if row else None
