import json

import cchardet
import peewee

from roles_api_pgsql.db import sync_pool


class BaseModel(peewee.Model):
    """Common db model"""
    class Meta:
        database = sync_pool


class UnknownField(object):
    def __init__(self, *_, **__): pass


def _decode_bytes(obj: bytes):
    try:
        coding = cchardet.detect(obj)
        encoding = coding['encoding']
    except Exception:
        return None
    if encoding is not None:
        return obj.decode(encoding)


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return _decode_bytes(obj)
        return json.JSONEncoder.default(self, obj)


class JSONField(peewee.TextField):
    def db_value(self, value):
        return json.dumps(value, cls=BytesEncoder)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)