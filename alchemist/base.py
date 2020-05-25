import os

from envyaml import EnvYAML

config_file = os.getenv("ALCHEMIST_CONFIG", "alchemist.yml")
config = EnvYAML(config_file, include_environment=False).export()
