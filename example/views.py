import datetime

from schema import Schema, And, Optional, Use, Regex
from flask_resource_tuner import MongoModelSchemaResource

from example.models import ExampleUsers, Gender


class DemoUserAPI(MongoModelSchemaResource):
    _model_ = ExampleUsers
    _create_schema_ = Schema(
        {
            "name": And(str, lambda s: 0 < len(s) < 10),
            Optional("phone"): str,
            "birthday": And(str, lambda s: datetime.datetime.fromisoformat(s)),
            "height": Use(float),
            "email": Regex(r"[0-9a-zA-z]*\@.*\.com"),
            "gender": Use(Gender),
            "pets": Schema(
                [{
                    "name": str,
                    "age": int
                }]
            )
        })
