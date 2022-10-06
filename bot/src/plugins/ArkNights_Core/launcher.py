from .config import Config

class Launcher:
    def __init__(self, config: Config) -> None:
        self._config = config
