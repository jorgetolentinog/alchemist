import os
import re
from collections import OrderedDict

PATH_DB = "db"
REGEX_SECTION = r"^(?:--\s\+migrate\s)(up|down)$"
REGEX_MIGRATION_FILE = r"^(\d{4})_(.+)\.sql$"


def path_migrations(db_name: str) -> str:
    return f"{PATH_DB}/{db_name}"


def parse_migrations(db_name: str) -> OrderedDict:
    directory = path_migrations(db_name)

    if not os.path.exists(directory):
        raise Exception("No parse because directory not exists: %s" % directory)

    parsed = OrderedDict()
    for filename in sorted(os.listdir(directory)):
        file_test = re.match(REGEX_MIGRATION_FILE, filename)
        if not file_test:
            continue

        version = file_test.group(1)
        parsed[version] = dict(
            description=file_test.group(2), up="", down="", apply=False,
        )

        with open(os.path.join(directory, filename), "r") as file_open:
            lines = file_open.read().split("\n")
            section_action = None

            for line in lines:
                section_test = re.match(REGEX_SECTION, line)
                if section_test:
                    section_action = section_test.group(1)

                if not section_action:
                    continue

                parsed[version][section_action] += f"{line}\n"

    return parsed
