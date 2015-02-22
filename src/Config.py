from configobj import ConfigObj


class Config(object):
    def __init__(self):
        self.readConfig()

    def readConfig(self):
        # read defaults
        self.config = ConfigObj('defaults.ini')

        # read override values        
        override = ConfigObj('override.ini')
        
        # merge overridden values into the config
        self.config.merge(override)
