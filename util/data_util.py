import csv


class DataUtil:
    @staticmethod
    def read_case_default_data(py_file_path, csv_file_name):
        csv_full_path = py_file_path.replace('case', r'data').replace('.py', '\\' + csv_file_name + '.csv')
        return DataUtil.read_csv_data(csv_full_path)

    @staticmethod
    def read_csv_data(file_path):
        r_list = []
        with open(file_path) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                a_map = map(lambda x, y: [x, y], header, row)
                dic = dict(a_map)
                # ignore case
                if 'skip' not in dic or dic['skip'] == 'N':
                    r_list.append(dic)
        return r_list

    @staticmethod
    def parse_default_data_file1(module, func_name):
        return '/'.join([module, func_name, 'yaml']).replace('case', 'data').split('.')

    @staticmethod
    def parse_default_data_file(fspath, func_name):
        return fspath.strpath.replace('case', 'data').replace('.py', r'\\' + func_name + '.csv')

    @staticmethod
    def read_case_default_data2(fspath, func_name):
        csv_full_path = fspath.strpath.replace('case', 'data').replace('.py', r'\\' + func_name + '.csv')
        return DataUtil.read_csv_data(csv_full_path)

    @staticmethod
    def parse_template_file(class_path):
        return class_path.replace('model', 'template').repace('.py', '.yaml')
