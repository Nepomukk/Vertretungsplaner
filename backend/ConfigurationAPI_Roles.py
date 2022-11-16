
from flask import render_template
from backend.ConfigurationManager_Roles import ConfigurationMngrRoles
from database.roles import Roles

class ConfigurationPages_Roles:
    def get_config_page(default):
        return render_template('pages/config_page.html', default=default)

    def get_config_roles_page(default):
        roles = ConfigurationMngrRoles.get_roles_objs()
        url: str = '/api/config/roles/del'
        return render_template('pages/config_roles_page.html', default=default, roles=roles, post_url=url)

    def config_roles_add_page(default):    
        placeholder_role = Roles(
            roleid=0,
            name='Bezeichnung',
            admin=False,
            level=1
        )
        url: str = '/api/config/roles/add'
        return render_template('pages/config_roles_edit_page.html', default=default, role=placeholder_role, action_title="Erstellen", post_url=url)

    def config_roles_edit_page(roleid: int, default):
        role_id: int = int(roleid)
        role = ConfigurationMngrRoles.get_role(role_id=role_id)
        url: str = '/api/config/roles/edit/'
        return render_template('pages/config_roles_edit_page.html', default=default, role=role, action_title="Bearbeiten", post_url=url)

class ConfigurationAPI_Roles:
    def config_roles_edit(form_data: dict, roldeid: int):
        ConfigurationMngrRoles.edit_role(
            roleid=roldeid,
            name=form_data.get('name', None),
            admin=form_data.get('admin', None),
            level=form_data.get('level', None)
        )

    def config_roles_del(role_id: int):
        ConfigurationMngrRoles.del_role(roleid=role_id)

    def config_roles_add(form_data: dict, role_id: int):
        ConfigurationMngrRoles.add_role(
            roleid=role_id,
            name=form_data.get('name', None),
            admin=form_data.get('admin', False),
            level=form_data.get('level', None)
        )
