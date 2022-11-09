from flask_restful_tuner import MongoModelSchemaResource

from example.models import ExampleUsers


class DemoUserAPI(MongoModelSchemaResource):
    _model_ = ExampleUsers
