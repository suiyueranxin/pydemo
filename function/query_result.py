from function.base import QueryObject
from model.request.anly.queryresult import QueryResultRequest
from model.static.metadata import Metadata


class QueryResult(QueryObject):
    def __init__(self, context):
        self.context = context
        self.record = context.payload
        self.pre_process()
        self.request = QueryResultRequest(self.context)
        QueryObject.__init__(self)
        pass

    @staticmethod
    def create_measure_axis():
        return Metadata.random_field('Measure')

    @staticmethod
    def create_dimension_axis():
        return Metadata.random_field('Dimension')

    @staticmethod
    def create_time_dimension_axis(time_type):
        return Metadata.random_time_field(time_type)

    def pre_process(self):
        temp_name = ','.join(self.record.keys())
        self.template.render(temp_name=temp_name, *self.record)
        for key in self.record:
            func_name = 'create_' + key
            if hasattr(self, func_name):
                func = getattr(func_name)
                func()
        self.context.payload = self.record

    def create_axes(self, **kwargs):
        need_update = False
        r_axes = []
        m_str, d_str = '', ''
        if 'm' in kwargs:
            measure_v = kwargs['m']
            if isinstance(measure_v, str):
                m_str = measure_v
            elif isinstance(measure_v, int) and measure_v == 1:
                m_str = self.create_measure_axis()
            else:
                print('error')

        if 'd' in kwargs:
            dimension_v = kwargs['d']
            if isinstance(dimension_v, str):
                d_str = dimension_v
            elif isinstance(dimension_v, int):
                if 'time' in kwargs:
                    d_str = self.create_time_dimension_axis(kwargs['time'])
                    if dimension_v == 2:
                        d_str += ',' + self.create_dimension_axis()
                else:
                    d_str = self.create_dimension_axis()
                    if dimension_v == 2:
                        d_str += ',' + self.create_dimension_axis()
            else:
                print('error')

        if m_str != '':
            need_update = True
            r_axes.append(m_str)

        if d_str != '':
            need_update = True
            r_axes.append(d_str)

        if need_update:
            self.record['axes'] = r_axes
        return ';'.join(r_axes)

    # "PostingYear,(EQUAL,1);DocumentTypeGroup, (EQUAL, Invoice)"
    def create_filters(self, **kwargs):
        r_filters = []
        filter_str = ''
        if 'time' in kwargs:
            filter_str = self.create_time_dimension_axis(kwargs['time'])