from dataclasses import field, dataclass
from marshmallow_dataclass import add_schema
from typing import Optional

from roles_api_pgsql.entities import Base, BaseEntity

# DON'T USE WORD SCHEMA IN NAMING. NEVER.


@add_schema(base_schema=Base)
@dataclass
class ResponseInternalError(BaseEntity):
    error: str = field(metadata=dict(required=True, allow_none=False, description="Error description"))


@add_schema(base_schema=Base)
@dataclass
class ResponseGetDummy(BaseEntity):
    name: str = field(metadata=dict(required=True,
                                    allow_none=False,
                                    description="Dummy name",
                                    example="lorem ipsum dummy sit amet"))

    nickname: Optional[str] = field(metadata=dict(required=False,
                                    allow_none=True,
                                    description="Dummy name",
                                    example="lorem ipsum dummy sit amet"))


@add_schema(base_schema=Base)
@dataclass
class ResponseGetDummyData(BaseEntity):
    data: ResponseGetDummy = field(metadata=dict(required=True, many=False))
