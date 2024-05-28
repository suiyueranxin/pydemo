from model.static.base import BaseStatic
import yaml


class RecentTime(BaseStatic):
    temp_file = 'recent_time.yaml'

    @classmethod
    def get_time(cls, *time):
        template = cls.get_template()
        time_type = time[0]
        return yaml.load(template.render(time=time))[time_type]

