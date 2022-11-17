import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import json
import sqlalchemy as db
from sqlalchemy import select
from typing import List, Any, NoReturn, Union
from database.roles import Roles, RoleSchema
from database.dbHelper import db

class ConfigurationMngrRoles:

    def get_roles_objs() -> List[Roles]:
        roles: List[Roles] = db.session.query(Roles).all()
        return roles

    def get_roles_dicts() -> List[RoleSchema]:
        role_objs: List[Roles] = ConfigurationMngrRoles.get_roles_objs()
        role_dicts: List[RoleSchema] = [role.to_dict() for role in role_objs]
        return role_dicts

    def get_role(role_id: int) -> Union[Roles, None]:
        role_objs: List[Roles] = ConfigurationMngrRoles.get_roles_objs()
        for role in role_objs:
            if role.roleid == role_id: return role
        return None

    def get_role_dict(role: Roles) -> RoleSchema:
        return role.to_dict()

    def del_role(roleid: int) -> NoReturn:
        role_to_delete = db.session.get(Roles, int(roleid))
        db.session.delete(role_to_delete)
        db.session.commit()

    def edit_role(roleid: int, name=None, admin=False, level=None) -> NoReturn:
        role_to_edit: Roles = db.session.get(Roles, int(roleid))
        role_to_edit.name = name
        role_to_edit.admin = admin
        role_to_edit.level = level
        db.session.commit()

    def add_role(
        name: str = 'role', 
        admin: Union[str, bool] = False, 
        level: Union[str, int] = 0,
        ) -> NoReturn:        
        db.session.add(
            Roles(name=name, level=int(level), admin=admin)
        )
        db.session.commit()

    def get_roles_json() -> str:
        return json.dumps(ConfigurationMngrRoles.get_roles_dicts())

    def get_role_json(role_id: int) -> str:
        return json.dumps(ConfigurationMngrRoles.get_role_dict(ConfigurationMngrRoles.get_role(role_id=role_id)))

