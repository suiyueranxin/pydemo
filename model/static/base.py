from jinja2 import Environment, PackageLoader
import yaml


class BaseStatic(object):
    @classmethod
    def register_template(cls):
        print('register_once')
        cls.temp_generator = Environment(loader=PackageLoader('template', 'static'))

    instance = None
    template = None

    @classmethod
    def get_template(cls):
        if cls.template is None:
            cls.template = cls.temp_generator.get_template(cls.temp_file)
        return cls.template

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = yaml.load(cls.temp_generator.get_template(cls.temp_file).render())
        return cls.instance

BaseStatic.register_template()

