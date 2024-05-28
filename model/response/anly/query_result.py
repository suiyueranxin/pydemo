from model.response.base import BaseResponse


class QueryResultResponse(BaseResponse):
    def __init__(self, context):
        self.temp_file = 'anly/query_result.yaml'
        BaseResponse.__init__(self, context)

    def get_body(self):
        return self.content

    def get_data(self):
        return self.data

    def get_fields(self):
        return [field['name'] for field in self.get_body()['metadata']['fields']]

    def count_fields(self):
        return len(self.get_fields())

    def count_data(self):
        return len(self.get_body()['data'])

    def has_fields(self):
        return self.count_fields() > 0

    time_fields = [
        'PostingYear',
        'PostingYearAndQuarter',
        'PostingYearAndMonth',
        'PostingYearAndWeek',
        'FiscalYear',
        'FinancialPeriodCode'
    ]

    def is_time_node(self, node):
        return len(node) > 1 and node[0]['v'].split['.'][1] in QueryResultCP.time_fields

    def is_zero_node(self, node):
        return self.is_time_node(node) and node[-1] == 0

    def zero_location(self):
        result = []
        # parse to get group of zero_index
        zero_index = []
        last_time, cur_time = '', ''
        index_group = []
        for index, node in self.get_data():
            if self.is_zero_node(node):
                cur_time = node[0]['d']
                if last_time == '':
                    last_time = cur_time
                if cur_time != last_time:
                    zero_index.append(index_group)
                    index_group = [index, ]
                    last_time = cur_time
                else:
                    index_group.append(index)
        # get zero result
        if 0 in zero_index[0]:
            result.append('start')
        for index_group in zero_index:
            if 0 < index_group[0] < len(self.get_data()) - 1:
                result.append('middle')
                break
        if len(self.get_data) - 1 in zero_index[-1]:
            result.append('end')
        return result

    def time_info(self):
        return set([node[0].d for node in self.data if self.is_time_node(node)])

    def time_range(self):
        time_list = [node[0].d for node in self.data if self.is_time_node(node)]
        return time_list[0], time_list[-1]