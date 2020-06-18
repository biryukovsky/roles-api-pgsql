# auto-generated snapshot
from peewee import *
import datetime
import peewee
snapshot = Snapshot()

@snapshot.append
class Role(peewee.Model):
    name = CharField(max_length=255, unique=True)
    readable = CharField(max_length=255)
    class Meta:
        table_name = "role"

