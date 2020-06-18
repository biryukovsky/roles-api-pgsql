from peewee import CharField

from roles_api_pgsql.models.base import BaseModel


class Role(BaseModel):
    name = CharField(unique=True)
    readable = CharField()
