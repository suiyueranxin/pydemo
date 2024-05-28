from model.request.base import BaseRequest


class LoginRequest(BaseRequest):
    def __init__(self, context):
        self.temp_file = 'auth/login.yaml'
        # super(BaseRequest, self).__init__()
        BaseRequest.__init__(self, context)
