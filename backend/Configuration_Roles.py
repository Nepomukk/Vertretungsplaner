import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import json
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Any, NoReturn, Union
from database.roles import Roles, RoleSchema
from database.dbHelper import Session

class ConfigurationRolesAPI:
    def get_roles_objs() -> List[Roles]:
        session: sessionmaker = Session.getSession()

        roles: List[Roles] = []

        role1 = Roles(0, 'role1', 1, False)
        role2 = Roles(1, 'role2', 2, True)
        roles.append(role1)
        roles.append(role2)
        return roles

    def get_roles_dicts() -> List[RoleSchema]: # todo
        role_objs: List[Roles] = ConfigurationRolesAPI.get_roles_objs()
        role_dicts: List[RoleSchema] = [role.to_dict() for role in role_objs]
        return role_dicts

    def get_role(role_id: int) -> Union[Roles, None]:
        role_objs: List[Roles] = ConfigurationRolesAPI.get_roles_objs()
        for role in role_objs:
            if role.roleid == role_id: return role
        return None

    def get_role_dict(role: Roles) -> RoleSchema:
        return role.to_dict()

    def del_role(roleid: int) -> NoReturn: # todo
        pass

    def edit_role(roleid: int, name=None, admin=False, level=None) -> NoReturn: # todo
        pass

    def add_role(roleid: int, name=None, admin=False, level=None) -> NoReturn: # todo
        pass

    def get_roles_json() -> str:
        return json.dumps(ConfigurationRolesAPI.get_roles_dicts())

    def get_role_json(role_id: int) -> str:
        return json.dumps(ConfigurationRolesAPI.get_role_dict(ConfigurationRolesAPI.get_role(role_id=role_id)))

