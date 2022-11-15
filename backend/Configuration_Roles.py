from model import Role
from typing import List, Any

class ConfigurationRoles():
    db_session: Any

    def __init__(self) -> None:
        self.db_session = "" # todo

    def get_roles_objs(self) -> List[Role.Role]:
        db_roles_data: Any

        roles: List[Role.Role]
        return roles

    def get_roles_dicts(self) -> List[Role.RoleSchema]:
        role_objs: List[Role.Role] = self.get_roles_objs()

        role_dicts: List[Role.RoleSchema] = [role.to_dict() for role in role_objs]
        return role_dicts

        