from .baseModel import Base

from sqlalchemy import Column, create_engine, Date, Identity, text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker

from typing import TypedDict, NoReturn


class RoleSchema(TypedDict):
    roleid: int
    name: str
    admin: bool
    level: int


class Roles(Base, object):
    __tablename__ = "roles"

    roleid = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False, unique=True)

    def __init__(self, roleid: int, name: str, level: int, admin: bool):
        self.roleid = roleid
        self.name = name
        self.level = level
        self.admin = admin

    def __repr__(self) -> str:
        return f"Roles(roleid={self.roleid!r}, " \
               f"name={self.name!r}, " \
               f"admin={self.admin!r}, " \
               f"level={self.level!r}, " \
               f")"

    def to_dict(self) -> RoleSchema:
        return {
            'roleid': self.roleid,
            'name': self.name,
            'admin': self.admin,
            'level': self.level
        }