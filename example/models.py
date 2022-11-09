from flask_restful_tuner.model import AutoUpdateDocument
from mongoengine.fields import FloatField, StringField, DateTimeField


class ExampleUsers(AutoUpdateDocument):
    meta = {"collection": "users_collection"}
    user_name = StringField()
    phone = StringField()
    birthday = DateTimeField()
    height = FloatField()
    weight = FloatField()
    address = StringField()
