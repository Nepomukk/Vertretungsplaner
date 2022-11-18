# from .baseModel import Base

# from sqlalchemy import Column, create_engine, Date, Identity, text
# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer
# from sqlalchemy import Boolean
# from sqlalchemy import String
# from sqlalchemy.dialects.postgresql import TIMESTAMP
# from sqlalchemy.orm import declarative_base, sessionmaker
# from werkzeug.security import generate_password_hash

# from typing import TypedDict, NoReturn


# class UserSchema(TypedDict):
#     userid: int
#     username: str
#     pwd: str
#     firstname: str
#     lastname: str
#     email: str


# class User(Base):
#     __tablename__ = "users"

#     userid = Column(Integer, nullable=False, primary_key=True)
#     username = Column(String, nullable=False)
#     pwd = Column(String, nullable=False)
#     firstname = Column(String, nullable=False)
#     lastname = Column(String, nullable=False)
#     email = Column(String, nullable=False)

#     def __init__(self, username: str, pwd:str, firstname: str, lastname: str, email: str):
#         self.username = username
#         self.pwd = generate_password_hash(pwd)
#         self.firstname = firstname
#         self.lastname = lastname
#         self.email = email

#     def __repr__(self):
#         return f"<User userid={self.userid!r}, " \
#                f"username={self.username!r}, " \
#                f"firstname={self.firstname!r}, " \
#                f"lastname={self.lastname!r}, " \
#                f"pwd={self.pwd!r}, " \
#                f"email={self.email!r}>"

#     def to_dict(self) -> UserSchema:
#         def set_dict(dictonary: dict, key: str) -> NoReturn:
#             dictonary[key] = getattr(self, key, None)

#         keys = UserSchema.__annotations__
#         result: UserSchema = dict
#         return [set_dict(result, key) for key in keys]
