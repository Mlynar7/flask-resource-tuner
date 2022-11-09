from flask_mongoengine import DynamicDocument
from mongoengine.fields import IntField

from flask_restful_tuner.utils import now_timestamp


class AutoUpdateDocument(DynamicDocument):
    meta = {"abstract": True, "ordering": "-created_time"}
    updated_time = IntField()
    created_time = IntField()

    def update(self, **kwargs):
        kwargs["updated_time"] = now_timestamp()
        return super(AutoUpdateDocument, self).update(**kwargs)

    def save(self, *args, **kwargs):
        kwargs["created_time"] = now_timestamp()
        return super(AutoUpdateDocument, self).save(*args, **kwargs)
