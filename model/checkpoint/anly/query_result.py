from dateutil.relativedelta import relativedelta
from datetime import date

from model.checkpoint.base import BaseCP
from model.static.metadata import Metadata


class QueryResultCP(BaseCP):
    def __init__(self, context):
        self.temp_file = 'anly/query_result.yaml'
        BaseCP.__init__(self, context)

    # time_info_str
    # months,4,3,2,1
    def pre_process_time_info(self):
        # todo support quarter
        r_time_info = []
        time_info_str = self.expected['time_info']
        time = time_info_str.split(',')
        time_type, time_delta = time[0], time[1:]
        rel = relativedelta()
        for delta in time_delta:
            setattr(rel, time_type, -(int(delta)-1))
            now = date.today() + rel
            r_time_info.append(self._format_time(now, time_type))
        self.expected['time_info'] = r_time_info
        return r_time_info

    def get_data(self):
        return self.actual['data']

    def get_fields(self):
        return [field['name'] for field in self.actual['metadata']['fields']]

    def count_fields(self):
        return len(self.get_fields())

    def count_data(self):
        return len(self.actual['data'])

    def has_fields(self):
        return self.count_fields() > 0

    def has_data(self):
        return self.count_data() > 0

    @staticmethod
    def is_time_node(node):
        return len(node) > 1 and Metadata.is_time_dim(node[0]['v'])

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
        if len(self.get_data()) - 1 in zero_index[-1]:
            result.append('end')
        return result

    def time_info(self):
        return [node[0]['d'] for node in self.get_data() if self.is_time_node(node)]

    def time_range(self):
        time_list = [node[0]['d'] for node in self.get_data() if self.is_time_node(node)]
        return time_list[0], time_list[-1]

    @staticmethod
    def _format_time(time, time_type):
        if time_type == "years":
            return "%04d" % time.year
        if time_type == "months":
            return "%04d-%02d" % (time.year, time.month)
        if time_type == "weeks":
            c = time.isocalendar()
            return "%04d%02d" % (c[0], c[1])