from alchemist.db import connection, cursor_fetchone

TABLE_VERSION_NAME = "version"


def create_version_table(db_name: str):
    cnx = connection(db_name)
    cnx.cursor().execute(
        f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_VERSION_NAME}' AND xtype='U')
            CREATE TABLE [{TABLE_VERSION_NAME}] (
                version VARCHAR(4) PRIMARY KEY NOT NULL,
                description VARCHAR(256) NOT NULL,
                applied_at DATETIME NOT NULL
            )
        """
    )
    cnx.commit()


def get_current_version_num(db_name: str) -> dict:
    create_version_table(db_name)
    cursor = connection(db_name).cursor()
    cursor.execute(
        f"SELECT ISNULL(MAX(version), 0) AS last_migration FROM [{TABLE_VERSION_NAME}]"
    )
    result = cursor_fetchone(cursor)
    return int(result["last_migration"])
