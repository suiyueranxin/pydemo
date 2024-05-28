from jinja2 import Environment, PackageLoader
import yaml

from aop.allure_step import Allurable


class BaseCP(Allurable):
    @classmethod
    def register_template(cls):
        print('register_once')
        cls.temp_generator = Environment(loader=PackageLoader('template', 'checkpoint'))
        pass

    def __init__(self, context):
        Allurable.__init__(self)
        if not hasattr(self, 'temp_file'):
            self.temp_file = 'base.yaml'
        self.template = None
        self.expected = context.case_cps
        self.actual = context.rsp_data
        self.status = context.rsp_status
        self.init_template()
        self.pre_process()

    def pre_process(self):
        # part1: parse key:value for expected values
        expected_str = self.expected.replace('\n', '')
        r_expected = {}
        if len(expected_str) > 0:
            cps_info = expected_str.split(';')
            for cp in cps_info:
                cp_func_name, cp_expected = cp.split(',', maxsplit=1)
                r_expected[cp_func_name] = cp_expected
        self.expected = r_expected
        # part2: pre_process for each expected value
        for key in self.expected:
            pre_func_name = 'pre_process_' + key
            if hasattr(self, pre_func_name):
                pre_func = getattr(self, pre_func_name)
                pre_func()

    def check(self):
        expected_str = self.template.render(self.expected)
        expected = yaml.load(expected_str)
        result = []
        pass_flag = True
        for func_name in expected:
            if expected.get(func_name) is not None:
                if hasattr(self, func_name):
                    func = getattr(self, func_name)
                    cp_actual = func()
                    cp_expected = expected.get(func_name)
                    try:
                        assert cp_actual == cp_expected
                        self.allure('check point: %s pass' % func_name)
                    except AssertionError:
                        pass_flag = False
                        fail_info = self.render_fail_info(func_name, cp_actual, cp_expected)
                        result.append(fail_info)
                        self.allure('check point: ' + fail_info)
                else:
                    result.append('cp_func %s not defined' % func_name)
                    self.allure('check point: cp_func %s not defined' % func_name)

        print('check', result)
        return pass_flag, result

    @staticmethod
    def render_fail_info(func_name, actual, expected):
        # todo assert fail template
        # self.template.render(func_name=func_name, actual=actual, expected=expected)
        return '%s fail, actual: %s, expected: %s' % (func_name, actual, expected)

    def status_code(self):
        return self.status

    def json_schema(self):
        # load template and check
        pass

    def json_all(self):
        # load template and check
        pass

    def has_node(self, json_path):
        pass

    def has_nodes(self, *json_path):
        pass

    def count_nodes(self):
        pass

    def init_template(self):
        self.template = BaseCP.temp_generator.get_template(self.temp_file)
        pass


BaseCP.register_template()

