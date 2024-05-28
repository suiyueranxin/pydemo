from requests import Session
from aop.allure_step import Allurable


class Context(Allurable):
    def __init__(self):
        self.session = Session()
        self.record = {}
        self.case_info = {}
        self.payload = {}
        self.case_cps = {}
        self.response = {}
        self.rsp_data = {}
        self.rsp_status = ''

    def set(self, info):
        # todo restore context during steps
        pass

    def get(self, key):
        # todo get context during steps
        pass

    def set_record(self, record):
        self.record = record
        self.parse_record()

    def parse_record(self):
        def _include(*keys):
            return {key: self.record[key] for key in keys}

        def _exclude(*keys):
            return {key: self.record[key] for key in self.record if key not in keys}

        self.case_info = _include('case_id', 'case_description', 'skip')
        self.payload = _exclude('case_id', 'case_name', 'case_description', 'skip', 'expected')
        self.case_cps = _include('expected').get('expected')
        # todo logging case_info
        self.allure('Case' + ': '.join(list(self.case_info.values())))

    def set_response(self, response):
        self.response = response
        self.parse_response()

    def parse_response(self):
        self.rsp_data = self.response.json()
        self.rsp_status = self.response.status_code
        pass

    # def allure(self):
    #     case_info_str = ": ".join(list(self.case_info.values()))
    #     with pytest.allure.step(case_info_str):
    #         print('allure_step', case_info_str)
