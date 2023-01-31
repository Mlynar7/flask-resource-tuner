from enum import Enum
from flask_resource_tuner.model import AutoUpdateDocument
from marshmallow_mongoengine.fields import Float, String, DateTime, List, Dict, Integer
from marshmallow_mongoengine.fields import Enum as EnumField


class Gender(Enum):
    Female = "F"
    Male = "M"
    Other = "O"


class PetInfo(Dict):
    name = String()
    age = Integer()


class ExampleUsers(AutoUpdateDocument):
    meta = {"collection": "users_collection"}
    name = String()
    phone = String()
    birthday = DateTime()
    height = Float()
    weight = Float()
    email = String()
    gender = EnumField(Gender, choices=[Gender.Male, Gender.Female, Gender.Other])
    pets = List(PetInfo())
