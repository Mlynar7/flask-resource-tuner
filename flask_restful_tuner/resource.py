import json
import logging as logger
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from flask_restful_tuner import validate_schema
from flask_restful_tuner import SysException

METHODS = ["get", "post", "put", "patch", "delete"]


class BaseResource(Resource):
    _validate_data_ = None
    _validate_schemas_ = {}

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        if meth not in METHODS:
            return SysException(message="SysMsg_gZ0kPdbz1",
                                status_code=HTTPStatus.METHOD_NOT_ALLOWED.value)

        request_data = request.json or json.loads(request.data) \
            if request.method.lower() not in ["get", "delete"] else request.args.to_dict()
        schema = self._validate_schemas_.get(request.method.lower())
        if schema:
            self._validate_data_, errors = validate_schema(schema, request_data)
            if errors:
                logger.info(errors)
                return SysException(message="SysMsg_YfPjErtc6",
                                    status_code=HTTPStatus.BAD_REQUEST.value)
        return super().dispatch_request(*args, **kwargs)

    def get(self):
        """
        get method
        """
        raise NotImplementedError

    def put(self):
        """
        put method
        """
        raise NotImplementedError

    def patch(self):
        """
        patch method
        """
        raise NotImplementedError

    def delete(self):
        """
        delete method
        """
        raise NotImplementedError
