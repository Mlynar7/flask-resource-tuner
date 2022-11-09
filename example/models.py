from enum import Enum
from flask_restful_tuner.model import AutoUpdateDocument
from mongoengine.fields import FloatField, StringField, DateTimeField, EnumField, ListField, DictField, IntField


class Gender(Enum):
    Female = "F"
    Male = "M"
    Other = "O"


class PetInfo(DictField):
    name = StringField()
    age = IntField()


class ExampleUsers(AutoUpdateDocument):
    meta = {"collection": "users_collection"}
    name = StringField()
    phone = StringField()
    birthday = DateTimeField()
    height = FloatField()
    weight = FloatField()
    email = StringField()
    gender = EnumField(Gender, choices=[Gender.Male, Gender.Female, Gender.Other])
    pets = ListField(PetInfo())
