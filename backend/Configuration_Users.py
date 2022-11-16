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
from database.dbHelper import Session

class ConfigurationUsersAPI:
    def get_users_objs() -> List[User]:
        session: sessionmaker = Session.getSession()

        users: List[User] = []

        user1 = User('user1', 'asd', 'firstname', 'lastname', 'eail', 0)
        users.append(user1)
        return users

    def get_users_dicts() -> List[UserSchema]:
        user_objs: List[User] = ConfigurationUsersAPI.get_users_objs()
        user_dicts: List[UserSchema] = [user.to_dict() for user in user_objs]
        return user_dicts

    def get_user(user_id: int) -> Union[User, None]:
        user_objs: List[User] = ConfigurationUsersAPI.get_users_objs()
        for user in user_objs:
            if user.userid == user_id: return user
        return None

    def get_user_dict(user: User) -> UserSchema:
        return user.to_dict()

    def del_user(userid: int) -> NoReturn: # todo
        pass

    def edit_user(
            userid: int, 
            username: str, 
            pwd: str, 
            firstname: str, 
            lastname: str,
            email: str
            ) -> NoReturn: # todo
        pass

    def add_user(
            userid: int, 
            username: str, 
            pwd: str, 
            firstname: str, 
            lastname: str,
            email: str
            ) -> NoReturn: # todo
        pass

    def get_users_json() -> str:
        return json.dumps(ConfigurationUsersAPI.get_users_dicts())

    def get_user_json(user_id: int) -> str:
        return json.dumps(ConfigurationUsersAPI.get_user_dict(ConfigurationUsersAPI.get_user(user_id=user_id)))

