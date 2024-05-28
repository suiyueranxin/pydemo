import allure


class Allurable(object):

    def __init__(self):
        self.allure(self.__class__.__name__)
        pass

    @staticmethod
    def allure(info_str):
        with allure.step(info_str):
            print('allure_step', info_str)
