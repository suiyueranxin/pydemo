from model.static.base import BaseStatic


class Metadata(BaseStatic):
    temp_file = 'metadata.yaml'

    @classmethod
    def get_id_and_type(cls, field):
        info = cls.get_info(field)
        return info[:2] if info is not None else None

    @classmethod
    def get_info(cls, field):
        instance = cls.get_instance()
        if field in instance["Measure"]:
            return instance["Measure"][field], 'MEASURE', None
        if field in instance["TimeDimension"]:
            return instance["TimeDimension"][field][0], 'DIMENSION', instance["TimeDimension"][field][1]
        if field in instance["Dimension"]:
            return instance["Dimension"][field], 'DIMENSION', None
        return None

    @classmethod
    def get_info_by_value(cls, value):
        # value: [FinancialPeriod].[FinancialPeriodCode].&[2018-05]
        field = value.split('.')[1][1:-1]
        return cls.get_info(field)

    @classmethod
    def is_time_dim(cls, value):
        info = cls.get_info_by_value(value)
        return True if len(info) == 3 and info[-1] is not None else False