import pyodbc

from alchemist import config

_connections = dict()


def cursor_row_as_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


class CursorWrapper:
    _cursor = None

    def __init__(self, conn):
        self._cursor = conn.cursor()

    def fetchone(self):
        row = self._cursor.fetchone()
        return cursor_row_as_dict(self._cursor, row) if row else None

    def fetchall(self):
        return [
            cursor_row_as_dict(self._cursor, row) for row in self._cursor.fetchall()
        ]

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            return getattr(self._cursor, name)(*args, **kwargs)

        return wrapper


class TransactionWrapper:
    _conn = None
    _cursor = None

    def __init__(self, conn):
        self._conn = conn
        self._cursor = CursorWrapper(self._conn)

    def __enter__(self):
        return self._cursor

    def __exit__(self, *args):
        if args[0]:
            self._conn.rollback()
            return

        self._conn.commit()


class ConnectWrapper:
    _conn = None

    def __init__(self, **kwargs):
        self._conn = pyodbc.connect(**kwargs)

    def cursor(self):
        return CursorWrapper(self._conn)

    def transaction(self):
        return TransactionWrapper(self._conn)


def connection(db_name: str) -> ConnectWrapper:
    """Get or create a connection"""

    if not _connections.get(db_name):
        db_config = config.databases.get(db_name)
        if not db_config:
            raise Exception("No config for %s database" % db_name)

        _connections[db_name] = ConnectWrapper(
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
