import json
from flask import Request
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.utils import cached_property

class Req(Request):
    """Request subclass to override request parameter storage"""
    __name__ = 'bam_request'
    parameter_storage_class = ImmutableOrderedMultiDict
    name = 'dp_flask_request'

    # @cached_property
    def json(self):
        """自定义request.get_json.当请求参数从GET-request.args中传入时,主动转移到request.get_json,
        """
        if self.method == 'GET':
            agrs = {}
            for k in self.args:
                agrs[k] = self.args[k]
            return agrs
        elif self.method == 'PUT':
            try:
                return json.loads(self.data.decode())
            except Exception as err:
                agrs = {}
                for k in self.form:
                    agrs[k] = self.form[k]
                return agrs
        else:
            return self.get_json()
