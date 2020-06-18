from dataclasses import field, dataclass
from typing import Optional
from marshmallow_dataclass import add_schema

from roles_api_pgsql.entities import Base, BaseEntity


@add_schema(base_schema=Base)
@dataclass
class RequestPostDummy(BaseEntity):
    name: str = field(metadata=dict(description='Name for new dummy', required=True, allow_none=False))
    nickname: Optional[str] = field(metadata=dict(description='Name for new dummy', required=False, allow_none=False))
