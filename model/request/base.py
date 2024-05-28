from jinja2 import Environment, PackageLoader
import random
import yaml
import json
import logging
import inflection

from config.config import Config
from aop.allure_step import Allurable

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


class BaseRequest(Allurable):
    @classmethod
    def register_template(cls):
        print('register_once')
        config = Config()
        cls.temp_generator = Environment(loader=PackageLoader('template', 'request'))
        cls.temp_generator.filters['parse_path'] = lambda path: '/'.join(
            [config.get('URL'), path]) if 'http://' not in path else path
        cls.temp_generator.filters['config'] = lambda key: config.get(key) if config.get(key) is not None else key
        cls.temp_generator.filters['random'] = lambda prefix: '_'.join([prefix, str(random.randint(1, 1000))])
        pass

    def __init__(self, context):
        Allurable.__init__(self)
        self.template = None
        self.session = context.session
        self.record = context.payload
        self._init_template()
        self.pre_process()

    def pre_process(self):
        for node_name in self.record:
            if self.record[node_name].strip() != '':
                func_name = 'pre_process_' + inflection.underscore(node_name)
                if hasattr(self, func_name):
                    pre_func = getattr(self, func_name)
                    pre_func()
            else:
                self.record[node_name] = None

    # def send(self):
    #     return self.send(self.record)

    def send(self):
        # todo: add try catch
        str_req = self.template.render(self.record)
        dic_req = yaml.load(str_req)
        if dic_req:
            if dic_req.get('method') == 'POST':
                return self._send_post(dic_req)
            else:
                return self._send_get(dic_req)
        return None

    def _send_post(self, dic_req):
        url = dic_req.get('path')
        payload = dic_req.get('payload')
        headers = dic_req.get('headers')
        # todo: using logging
        self._log(url, json.dumps(payload))
        return self.session.post(url, headers=headers, data=json.dumps(payload))

    def _send_get(self, dic_req):
        url = '/'.join([Config().get('TEST.URL'), dic_req.get('path')])
        payload = dic_req.get('payload')
        headers = dic_req.get('headers')
        return self.session.get(url, headers=headers, params=payload)

    def _init_template(self):
        self.template = BaseRequest.temp_generator.get_template(self.temp_file)
        pass

    @staticmethod
    def _log(url, payload):
        print('url', url)
        print('payload', payload)
        

BaseRequest.register_template()

