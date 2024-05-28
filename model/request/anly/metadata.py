import pytest
from model.request.base import BaseRequest


class MetaDataRequest(BaseRequest):
    def __init__(self, context):
        self.temp_file = 'anly/model_metadata.yaml'
        BaseRequest.__init__(self, context)
        # with pytest.allure.step(self.__module__):
        #     self.send()
