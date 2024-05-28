import pytest
from case.base import BaseTestCase
from model.request.anly.queryresult import QueryResultRequest
from model.checkpoint.anly.query_result import QueryResultCP


class TestQueryResult(BaseTestCase):

    @pytest.mark.parametrize('case_data', BaseTestCase.prepare_data(__file__, 'kpi_line_chart_card'))
    def test_kpi_line_chart_card(self, case_data):
        # todo save record in context
        self.context.set_record(case_data)

        req = QueryResultRequest(self.context)
        rsp = req.send()

        self.context.set_response(rsp)
        cps = QueryResultCP(self.context)
        flag, details = cps.check()

        assert flag, details
