import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import json
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Any, NoReturn, Union
from database.users import User, UserSchema
from database.dbHelper import db

class ConfigurationMngrUsers:
    def get_users_objs() -> List[User]:

        users: List[User] = db.session.query(User).all()
        return users

    def get_users_dicts() -> List[UserSchema]:
        user_objs: List[User] = ConfigurationMngrUsers.get_users_objs()
        user_dicts: List[UserSchema] = [user.to_dict() for user in user_objs]
        return user_dicts

    def get_user(user_id: int) -> Union[User, None]:
        user_objs: List[User] = ConfigurationMngrUsers.get_users_objs()
        for user in user_objs:
            if user.userid == user_id: return user
        return None

    def get_user_dict(user: User) -> UserSchema:
        return user.to_dict()

    def del_user(userid: Union[str, int]) -> NoReturn:
        user_to_delete = db.session.get(User, int(userid))
        db.session.delete(user_to_delete)
        db.session.commit()

    def edit_user(
            userid: int, 
            username: str, 
            pwd: str, 
            firstname: str, 
            lastname: str,
            email: str
            ) -> NoReturn:
        user_to_edit: User = db.session.get(User, int(userid))
        user_to_edit.username = username
        user_to_edit.pwd = pwd
        user_to_edit.firstname = firstname
        user_to_edit.lastname = lastname
        user_to_edit.email = email
        db.session.commit()

    def add_user(
            username: str, 
            pwd: str, 
            firstname: str, 
            lastname: str,
            email: str
            ) -> NoReturn:
        db.session.add(
            User(
                username=username, 
                pwd=pwd, 
                firstname=firstname,
                lastname=lastname,
                email=email
            )
        )
        db.session.commit()

    def get_users_json() -> str:
        return json.dumps(ConfigurationMngrUsers.get_users_dicts())

    def get_user_json(user_id: int) -> str:
        return json.dumps(ConfigurationMngrUsers.get_user_dict(ConfigurationMngrUsers.get_user(user_id=user_id)))

