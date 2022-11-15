from types import Union
from typing import TypedDict

class RoleSchema(TypedDict):
    name: str
    level: int
    admin: Union[bool, int]


class Role():
    name: str
    level: int
    admin: Union[bool, int]

    def __init__(self, name: str, level: int, admin: bool):
        self.name = name
        self.level = level
        self.admin = admin

    def to_dict(self) -> RoleSchema:
        my_keys = RoleSchema.keys
        my_dict: RoleSchema = dict

        [setattr(my_dict, key, getattr(self, key)) = getattr(self, key) for key in my_keys]

        return my_dict
