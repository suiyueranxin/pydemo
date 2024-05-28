import pytest
from case.base import BaseTestCase
from function.query_result import QueryResult
from model.checkpoint.anly.query_result import QueryResultCP


class TestGlobalFilters(BaseTestCase):

    @pytest.mark.parametrize('case_data', BaseTestCase.prepare_data(__file__, 'posting_date'))
    def test_crud(self, case_data):
        # todo save record in context
        self.context.set_record(case_data)

        req = QueryResult(self.context)
        rsp = req.send()

        self.context.set_response(rsp)
        cps = QueryResultCP(self.context)
        flag, details = cps.check()

        assert flag, details


    def test_zero_auto_range(self, case_data):
        pass



