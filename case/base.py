import pytest
from util.data_util import DataUtil
from case.context import Context
from model.request.auth.login import LoginRequest


class BaseTestCase(object):
    @staticmethod
    def prepare_data(run_file, file_name):
        return DataUtil.read_case_default_data(run_file, file_name)

    @staticmethod
    def prepare_multi_data(run_file, list_file_names):
        r_data = {}
        for file_name in list_file_names:
            r_data[file_name] = BaseTestCase.prepare_data(run_file, file_name)
        return r_data

    @pytest.fixture(scope='class', autouse=False)
    def init_class(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def init_context(self):
        self.context = Context()
        LoginRequest(self.context).send()

