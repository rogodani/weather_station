from configparser import ConfigParser
import os


class SetupParser:

    def __init__(self, section, filename="setup.ini"):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.filename = filename
        self.section = section

    def get_param(self):
        parser = ConfigParser()
        parser.read(self.filename)
        if parser.has_section(self.section):
            return {key: value for (key, value) in parser.items(self.section)}
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))


if __name__ == '__main__':
    print(SetupParser("postgresql").get_param())
