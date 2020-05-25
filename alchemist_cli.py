import argparse
import sys

from alchemist.db.migrate import runner as migrate_runner


def migrate_database(argument):
    commands = ['upgrade', 'downgrade']
    for cmd in commands:
        bases = getattr(argument, cmd)
        if not bases:
            continue

        for db_name in bases:
            print(f'db - {db_name}')
            getattr(migrate_runner, cmd)(db_name=db_name)


# parser
parser = argparse.ArgumentParser()
sub = parser.add_subparsers()

# parser for the "migrate" command
parser_migrate = sub.add_parser("migrate")
parser_migrate.set_defaults(func=migrate_database)
parser_migrate_group = parser_migrate.add_mutually_exclusive_group(required=True)
parser_migrate_group.add_argument(
    "--upgrade", metavar="db", nargs="+", help="upgrade migrations",
)
parser_migrate_group.add_argument(
    "--downgrade", metavar="db", nargs="+", help="downgrade migrations",
)

if __name__ == "__main__":
    args_parsed = parser.parse_args()
    if not hasattr(args_parsed, "func"):
        parser.print_help()
        sys.exit()

    args_parsed.func(args_parsed)
