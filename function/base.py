from aop.allure_step import Allurable


class QueryObject(Allurable):
    def __init__(self, context):
        self.request.send()
        pass

    def create(self):
        pass

    def retrieve(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def create(self, n):
        pass



