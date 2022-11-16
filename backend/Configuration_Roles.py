import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from database.dbHelper import Roles, RoleSchema
from typing import List, Any, NoReturn
from database import dbHelper

class ConfigurationRoles(object):
    session: dbHelper.Session

    def __init__(self) -> NoReturn:
        self.db_session = dbHelper.Session.getSession()

    def get_roles_objs(self) -> List[Roles]:
        db_roles_data: Any = self.db_session

        roles: List[Roles.Role]
        return roles

    def get_roles_dicts(self) -> List[RoleSchema]:
        role_objs: List[Roles.Role] = self.get_roles_objs()

        role_dicts: List[Roles.RoleSchema] = [role.to_dict() for role in role_objs]
        return role_dicts

        
test = ConfigurationRoles().get_roles_objs()
print("asd")