from jinja2 import Environment, PackageLoader
from model.response.http_status import HttpStatus


class BaseResponse(object):
    @classmethod
    def register_template(cls):
        print('register_once')
        cls.temp_generator = Environment(loader=PackageLoader('template', 'response'))
        pass

    def __init__(self, context):
        self.content = context.content
        self._init_template()

    def status_success(self):
        return self.content.status_code == HttpStatus['success']

    def json_schema(self):
        # todo load template and check
        pass

    def json_all(self):
        # todo load template and check
        pass

    def _init_template(self):
        self.template = BaseResponse.temp_generator.get_template(self.temp_file)
        pass


BaseResponse.register_template()