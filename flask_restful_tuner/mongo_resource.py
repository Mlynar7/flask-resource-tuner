from http import HTTPStatus
from schema import Schema
from marshmallow_mongoengine import ModelSchema

from flask_restful_tuner.resource import BaseResource
from flask_restful_tuner.exception import SysException
from flask_restful_tuner import logger

FILTER_OPERATOR_MAP = {
    ">": "__gt",
    "<": "__lt",
    ">=": "__gte",
    "<=": "__lte",
    "!=": "__ne",
    "==": "",
    "contains": "__contains",
}


class MongoModelResource(BaseResource):
    # pk
    _pk_ = "id"
    # db model
    _model_ = None

    # list response schema
    _list_item_schema_: Schema = None

    # detail response schema, use for create\put\patch\get(with pk)
    _detail_schema_: Schema = None

    # query params
    _filters_: list = []

    # pagination
    _max_page_size_: int = 100
    _default_page_size_: int = 10

    # create schema
    _create_schema_: Schema = None

    # query schema
    _query_schema_: Schema = None

    # update schema
    _update_schema_: Schema = None

    # validate
    _validate_schemas_ = {
        "post": _create_schema_,
        "get": _query_schema_,
        "put": _update_schema_,
        "patch": _update_schema_,
        "delete": None
    }

    def post(self):
        instance, errors = self._create_schema_.load(self._validate_data_)
        if errors:
            logger.error(errors)
            raise SysException(message="SysMsg_KbjM8gnOq", status_code=HTTPStatus.BAD_REQUEST.value)
        instance.save()
        data, errors = self._detail_schema_.dump(instance)
        if errors:
            logger.error(errors)
            raise SysException(message="SysMsg_gTvqCf1tl", status_code=HTTPStatus.BAD_REQUEST.value)
        return data

    def delete(self):
        pk = self._validate_data_.get(self._pk_)
        instance = self._model_.objects.filter(pk=pk).first()
        if not instance:
            raise SysException(message="SysMsg_J0y5Hr8RA", status_code=HTTPStatus.NOT_FOUND.value)
        instance.delete()

    def prepare_for_update(self, instance):
        return self._validate_data_

    def put(self):
        instance = self._model_.objects.filter(pk=self._validate_data_.pop(self._pk_)).first()
        if not instance:
            raise SysException(message="SysMsg_ihwnxWCk1", status_code=HTTPStatus.NOT_FOUND.value)

        instance, errors = self._update_schema_.update(instance, self.prepare_for_update(instance))
        if errors:
            logger.error(errors)
            raise SysException(message="SysMsg_dhfRSWtnj", status_code=HTTPStatus.BAD_REQUEST.value)

        instance.save()
        data, errors = self._detail_schema_.dump(instance)
        if errors:
            logger.error(errors)
            raise SysException(message="SysMsg_fJ6rUZxNY", status_code=HTTPStatus.BAD_REQUEST.value)
        return data

    def patch(self):
        return self.put()

    def get_queryset(self):
        conditions = {}
        for filter_field in self._filters_:
            column, op, field, convert_fn = filter_field
            value = self._validate_data_.get(field)
            converted_value = convert_fn(value) if convert_fn else value
            operator = FILTER_OPERATOR_MAP[op]
            conditions["{column}{operator}".format(column=column, operator=operator)] = converted_value
        return self._model_.objects.filter(**conditions)

    def get(self):
        queryset = self.get_queryset()

        by_pk = self._validate_data_.get(self._pk_)
        if by_pk:
            instance = queryset.filter(pk=by_pk).first()
            if not instance:
                return {}
            data, errors = self._detail_schema_.dump(instance)
            if errors:
                logger.error(errors)
                raise SysException(message="SysMsg_R6GlHOdZ0", status_code=HTTPStatus.BAD_REQUEST.value)
            return data
        else:
            page = self._validate_data_.get("page", 1)
            page_size = min(self._validate_data_.get("page_size", self._default_page_size_), self._max_page_size_)
            pagination = queryset.paginate(page=page, per_page=page_size)
            ret_list = []
            for item in pagination.items:
                data, errors = self._list_item_schema_.dump(item)
                if errors:
                    logger.error(errors)
                    raise SysException(message="SysMsg_jHBdky60Q", status_code=HTTPStatus.BAD_REQUEST.value)
                ret_list.append(data)

            return {
                "total": pagination.total,
                "pages": pagination.pages,
                "page": pagination.page,
                "page_size": page_size,
                "results": ret_list,
            }


class MongoModelSchemaResource(MongoModelResource):
    def dispatch_request(self, *args, **kwargs):
        meta = type("Meta", (object,), dict(model=self._model_))
        schema = type("Schema", (ModelSchema,), dict(Meta=meta))
        self._update_schema_ = schema()
        self._create_schema_ = schema()
        self._query_schema_ = schema()
        self._detail_schema_ = schema()
        return super().dispatch_request(*args, **kwargs)
