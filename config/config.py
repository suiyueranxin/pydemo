import configparser
import os

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_INI_PATH = os.path.join(CONFIG_PATH, 'config.ini')


class Config(object):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_INI_PATH)

    def __init__(self):
        self.__env = Config.parser['BASE']['ENV']
        self.props = configparser.ConfigParser()
        self.props.read(os.path.join(CONFIG_PATH, self.__env + '.ini'))

    def get(self, prop_name):
        # support section.option or option
        prop_dot_path = prop_name.split('.')
        if len(prop_dot_path) > 1:
            section = prop_dot_path[0].upper()
            option = prop_dot_path[1].upper()
            return self.props[section][option]
        else:
            return self.props['TEST'][prop_name.upper()]


