from alchemist.db.base import connection

TABLE_VERSION_NAME = "version"


def create_version_table(db_name: str):
    with connection(db_name).transaction() as cursor:
        cursor.execute(
            f"""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_VERSION_NAME}' AND xtype='U')
                CREATE TABLE [{TABLE_VERSION_NAME}] (
                    version VARCHAR(4) PRIMARY KEY NOT NULL,
                    description VARCHAR(256) NOT NULL,
                    applied_at DATETIME NOT NULL
                )
            """
        )


def get_current_version_num(db_name: str) -> dict:
    create_version_table(db_name)
    cursor = connection(db_name).cursor()
    cursor.execute(
        f"SELECT ISNULL(MAX(version), 0) AS last_migration FROM [{TABLE_VERSION_NAME}]"
    )
    result = cursor.fetchone()
    return int(result["last_migration"])
