import json
from flask import make_response


class SysException(BaseException):
    def __init__(self, code=-1, message="", status_code=200):
        self.code = code
        self.status_code = status_code
        self.message = message

    def get_response(self):
        return make_response(json.dumps({"code": self.code,
                                         "message": self.message,
                                         "data": {}}), self.status_code)
