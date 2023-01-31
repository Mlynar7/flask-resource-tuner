import json
import logging as logger
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from flask_resource_tuner.validator import validate_schema
from flask_resource_tuner.exception import SysException

METHODS = ["get", "post", "put", "patch", "delete"]


class BaseResource(Resource):
    _validate_data_ = None
    _validate_schemas_ = {}

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask
        meth = request.method.lower()
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        if meth not in METHODS:
            raise SysException(message="SysMsg_gZ0kPdbz1",
                               status_code=HTTPStatus.METHOD_NOT_ALLOWED.value)

        request_data = request.json or json.loads(request.data) \
            if request.method.lower() not in ["get", "delete"] else request.args.to_dict()
        schema_attr = self._validate_schemas_.get(request.method.lower())
        if schema_attr:
            self._validate_data_, errors = validate_schema(getattr(self, schema_attr), request_data)
            if errors:
                logger.error(errors)
                raise SysException(message="SysMsg_YfPjErtc6",
                                   status_code=HTTPStatus.BAD_REQUEST.value)
        else:
            self._validate_data_ = {}
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
