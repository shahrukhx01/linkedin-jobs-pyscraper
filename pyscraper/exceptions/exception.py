class InvalidConfigurationException(Exception):
    """Raised when an invalid configuration file is set"""

    def __init__(self, *args):
        super().__init__(*args)