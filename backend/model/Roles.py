from sqlalchemy import Column, create_engine, Date, Identity, text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import psycopg2, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker

from typing import TypedDict, NoReturn

from backend.model.ModelBase import Base

Base = declarative_base()

class RoleSchema(TypedDict):
    roleid: int
    name: str
    admin: bool
    level: int


class Roles(Base):
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
        def set_dict(dictonary: dict, key: str) -> NoReturn:
            dictonary[key] = getattr(self, key, None)

        keys = RoleSchema.__annotations__
        result: RoleSchema = dict   
        return [set_dict(result, key) for key in keys]