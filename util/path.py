import os
import sys


class Path:
    @staticmethod
    def get_full_path(call_o):
        return os.path.dirname(call_o.__file__)

    @staticmethod
    def get_parent_path(call_o):
        return os.path.dirname(os.path.abspath(call_o.__file__))

    @staticmethod
    def get_root_path():
        return sys.path[0]

    @staticmethod
    def get_file_path(call_o, file_name):
        return os.path.join(Path.get_parent_path(call_o), file_name)