import os

from envyaml import EnvYAML

_config_file = os.getenv("ALCHEMIST_CONFIG", "alchemist.yml")
_config = EnvYAML(_config_file, include_environment=False).export()

for _key, _value in _config.items():
    globals()[_key] = _value
