from backend.model import Roles
from typing import List, Any, NoReturn
from database import dbHelper

class ConfigurationRoles():
    session: dbHelper.Session

    def __init__(self) -> NoReturn:
        self.db_session = dbHelper.Session.getSession()

    def get_roles_objs(self) -> List[Roles.Role]:
        db_roles_data: Any = self.session.getSession()

        roles: List[Roles.Role]
        return roles

    def get_roles_dicts(self) -> List[Roles.RoleSchema]:
        role_objs: List[Roles.Role] = self.get_roles_objs()

        role_dicts: List[Roles.RoleSchema] = [role.to_dict() for role in role_objs]
        return role_dicts

        