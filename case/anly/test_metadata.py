import pytest
from case.base import BaseTestCase
from model.request.anly.metadata import MetaDataRequest
from model.checkpoint.base import BaseCP


class TestMetadata(BaseTestCase):

    @pytest.mark.parametrize('case_data', BaseTestCase.prepare_data(__file__, 'metadata'))
    def test_all_metadata(self, case_data):
        self.context.set_record(case_data)

        req = MetaDataRequest(self.context)
        rsp = req.send()

        self.context.set_response(rsp)
        cps = BaseCP(self.context)
        flag, details = cps.check()

        assert flag, details



