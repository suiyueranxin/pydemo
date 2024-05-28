from model.request.base import BaseRequest
from model.static.metadata import Metadata
from model.static.recent_time import RecentTime


class QueryResultRequest(BaseRequest):
    def __init__(self, context):
        self.temp_file = 'anly/query_result.yaml'
        BaseRequest.__init__(self, context)

    # axes_str:
    # "NetSalesAmountLC,SUM;PostingYear"
    def pre_process_axes(self):
        # todo get str from record
        axes_str = self.record['axes'].replace('\n', '')
        r_axes = []
        axes = axes_str.split(';')
        for axis_info in axes:
            axis = {}
            info = axis_info.split(',')
            label = info[0]
            axis['id'], axis['type'] = Metadata.get_id_and_type(label)
            if len(info) > 1:
                axis['aggregation'] = info[-1]
            r_axes.append(axis)
        # todo update record
        self.record['axes'] = r_axes
        print('axes', r_axes)
        return r_axes

    # filters_str:
    # PostingDate,(BT,20160101,20180731),(EQUAL,20150101);
    # DocumentType,(EQUAL,Invoice),(EQUAL,Delivery);
    # BusinessPartnerCode,(EQUAL,C23900),(EQUAL,C60000)
    def pre_process_filters(self):
        filters_str = self.record['filters'].replace('\n', '')
        r_filters = []
        filters = filters_str.split(';')
        for filter_info in filters:
            filter_item = []
            info = filter_info.split(',(')
            label = info[0]
            ana_id, ana_type, ana_time_type = Metadata.get_info(label)
            conditions = info[1:]
            for condition_info in conditions:
                condition = {}
                c_info = condition_info[:-1].split(',')
                condition['analysisObjectId'] = ana_id
                condition['operator'] = c_info[0]
                condition['members'] = [RecentTime.get_time(ana_time_type, m) for m in c_info[1:]] if ana_time_type else c_info[1:]
                filter_item.append(condition)
            r_filters.append(filter_item)
        self.record['filters'] = r_filters
        print('filters', r_filters)
        return r_filters

    # order_by_str:
    # PostingYear,DESC
    # NetSalesAmountLC,DESC
    def pre_process_order_by(self):
        order_by_str = self.record['orderBy']
        r_order_by = {
            'id': None,
            'measureId': None,
            'flag': 'ASC'
        }
        info = order_by_str.split(',')
        ana_id, ana_type = Metadata.get_id_and_type(info[0])
        if ana_type == 'DIMENSION':
            r_order_by['id'] = ana_id
        else:
            r_order_by['measureId'] = ana_id
        if len(info) > 1:
            r_order_by['flag'] = info[1]
        self.record['orderBy'] = r_order_by
        print('orderBy', r_order_by)
        return r_order_by

    # zero_complements_str:
    # year,5,1
    def pre_process_zero_complements(self):
        zero_complements_str = self.record['zeroComplements']
        r_zero_complements = {}
        time_type, start_date, end_date = zero_complements_str.split(',')
        r_zero_complements['startDate'] = RecentTime.get_time(time_type, start_date)
        r_zero_complements['endDate'] = RecentTime.get_time(time_type, end_date)
        self.record['zeroComplements'] = r_zero_complements
        print('zeroComplements', r_zero_complements)
        return r_zero_complements
