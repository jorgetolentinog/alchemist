from collections import OrderedDict

from alchemist.db.base import connection

from .parse import parse_migrations
from .version import get_current_version_num


def migrations_status(db_name: str) -> OrderedDict:
    current_version = get_current_version_num(db_name)
    migrations = parse_migrations(db_name)

    for version in migrations.keys():
        if current_version >= int(version):
            migrations[version]["apply"] = True

    return migrations


def log_step(version, description, script):
    print(f"{version} - {description}\n")
    print(script, "-" * 79)


def upgrade(db_name: str):
    migrations = migrations_status(db_name)
    cursor = connection(db_name).cursor()

    with connection(db_name).transaction() as cursor:
        for version, migration in migrations.items():
            if migration["apply"]:
                continue

            description = migration["description"]
            script = migration["up"]
            log_step(
                version=version, description=description, script=script,
            )

            cursor.execute(script)
            cursor.execute(
                "INSERT INTO version (version, description, applied_at) VALUES (?, ?, GETDATE())",
                (version, description),
            )


def downgrade(db_name: str):
    migrations = migrations_status(db_name)

    last_version = None
    last_migration = None

    for version, migration in migrations.items():
        if not migrations[version]["apply"]:
            continue

        last_version = version
        last_migration = migration

    if not last_version:
        print("No migrations found for downgrade")
        return

    script = last_migration["down"]
    log_step(
        version=last_version, description=last_migration["description"], script=script,
    )

    with connection(db_name).transaction() as cursor:
        cursor.execute(script)
        cursor.execute("DELETE FROM version WHERE version = ?", last_version)
