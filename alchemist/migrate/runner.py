from collections import OrderedDict

from alchemist.db import connection

from .parse import parse_migrations
from .version import get_current_version_num


def migrations_status(db_name: str) -> OrderedDict:
    current_version = get_current_version_num(db_name)
    migrations = parse_migrations(db_name)

    for version in migrations.keys():
        if current_version >= int(version):
            migrations[version]["apply"] = True

    return migrations


def upgrade(db_name: str):
    migrations = migrations_status(db_name)
    cursor = connection(db_name).cursor()

    try:
        for version, migration in migrations.items():
            if migration["apply"]:
                continue

            description = migration["description"]
            script = migration["up"]
            step_log(
                version=version, description=description, script=script,
            )

            cursor.execute(script)
            cursor.execute(
                "INSERT INTO version (version, description, applied_at) VALUES (?, ?, GETDATE())",
                (version, description),
            )

        cursor.commit()
    except Exception as e:
        cursor.rollback()
        raise e


def downgrade(db_name: str):
    migrations = migrations_status(db_name)
    cursor = connection(db_name).cursor()

    try:
        last_version = None
        last_migration = None

        for version, migration in migrations.items():
            if not migrations[version]["apply"]:
                continue

            last_version = version
            last_migration = migration

        if not last_version:
            exit("No migrations found for downgrade")

        script = last_migration["down"]
        step_log(
            version=last_version,
            description=last_migration["description"],
            script=script,
        )

        cursor.execute(script)
        cursor.execute("DELETE FROM version WHERE version = ?", last_version)

        cursor.commit()
    except Exception as e:
        cursor.rollback()
        raise e


def step_log(version, description, script):
    print(f"{version} - {description}\n")
    print(script, "-" * 79)
