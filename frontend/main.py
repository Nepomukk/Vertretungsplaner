import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import json
import os
from typing import List, TypedDict, Union

import flask
from flask import jsonify, render_template, request, Response

# Roles
from backend.Configuration_Roles import ConfigurationRolesAPI, Roles
from backend.Configuration_Users import ConfigurationUsersAPI, User
from database.dbHelper import Session

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# load all file names from the respective folder to automatically add all files within
js_files = os.listdir('frontend/static/js')
css_files = os.listdir('frontend/static/css')

menu_items = {
    'formular': {
        'name': 'Formular erstellen',
        'path': '/formular',
        'icon': 'fa-solid fa-file-circle-plus',
    },
}

# add to default var set for all templates
default = {
    "js_files": js_files,
    "css_files": css_files,
    "menu_items": menu_items,
}

# INFO: add hide_menu=True to render_template() to disable the menu for a route


@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', default=default, username=name)

# ############################################################ A6 Konfiguration Page Endpoints - ROLES
@app.route('/config/roles') # get page config-roles
def get_config_roles_page():
    roles = ConfigurationRolesAPI.get_roles_objs()
    url: str = '/api/config/roles/del'
    return render_template('pages/config_roles_page.html', default=default, roles=roles, post_url=url)

@app.route('/config/roles/add') # get page add role
def config_roles_add_page():    
    role = Roles( # todo
        roleid=0,
        name='Bezeichnung',
        admin=False,
        level=1
    )
    url: str = '/api/config/roles/add'
    return render_template('pages/config_roles_edit_page.html', default=default, role=role, action_title="Erstellen", post_url=url)

@app.route('/config/roles/edit/<roleid>', methods=['GET']) # get page edit role
def config_roles_edit_page(roleid: str):
    role_id: int = int(roleid)
    role = ConfigurationRolesAPI.get_role(role_id=role_id)
    url: str = '/api/config/roles/edit/'
    return render_template('pages/config_roles_edit_page.html', default=default, role=role, action_title="Bearbeiten", post_url=url)

@app.route('/api/config/roles/edit/', methods=['POST']) # edit role
def config_roles_edit():
    try:
        form_data = request.form
        roldeid: int = int(form_data.get('roleid', None))

        role = ConfigurationRolesAPI.get_role(role_id=roldeid)
        url: str = '/api/config/roles/edit/'

        ConfigurationRolesAPI.edit_role(
            roleid=roldeid,
            name=form_data.get('name', None),
            admin=form_data.get('admin', None),
            level=form_data.get('level', None)
        )
        return render_template('pages/config_roles_edit_page.html', default=default, role=role, action_title="Bearbeiten", post_url=url)
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/roles/del/<roleid>', methods=['POST']) # del role
def config_roles_del(roleid: str):
    url: str = '/api/config/roles/del/<roleid>'
    role_id: int = int(roleid)

    try:
        url: str = '/api/config/roles/del/<roleid>'
        role_id: int = int(roleid)

        ConfigurationRolesAPI.del_role(roleid=role_id)
        url: str = '/api/config/roles/del'
        roles = ConfigurationRolesAPI.get_roles_objs()
        return render_template('pages/config_roles_page.html', default=default, roles=roles, post_url=url)
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/roles/add/', methods=['POST']) # add role
def config_roles_add():
    try:
        form_data = request.form
        roldeid: int = int(form_data.get('roleid', 0))

        role = ConfigurationRolesAPI.get_role(role_id=roldeid)
        url: str = '/api/config/roles/add'

        ConfigurationRolesAPI.add_role(
            roleid=roldeid,
            name=form_data.get('name', None),
            admin=form_data.get('admin', False),
            level=form_data.get('level', None)
        )
        return render_template('pages/config_roles_edit_page.html', default=default, role=role, action_title="Bearbeiten", post_url=url)
    except:
        resp = Response("invalid request", status=400)
        return resp
# ############################################################ A6 Konfiguration Page Endpoints - ROLES \

# ############################################################ A6 Konfiguration Page Endpoints - USERS
@app.route('/config/users') # get page config-users
def get_config_users_page():
    users = ConfigurationUsersAPI.get_users_objs()
    url: str = '/api/config/roles/del'
    return render_template('pages/config_users_page.html', default=default, users=users, post_url=url)

@app.route('/config/users/edit/<userid>', methods=['GET']) # get page edit role
def config_users_edit_page(userid: str):
    user_id: int = int(userid)
    user = ConfigurationUsersAPI.get_user(user_id=user_id)
    url: str = '/api/config/users/edit/'
    return render_template('pages/config_users_edit_page.html', default=default, user=user, action_title="Bearbeiten", post_url=url)

@app.route('/config/users/add') # get page add role
def config_users_add_page():
    user = User(
        userid=0,
        username='Benutzername',
        pwd='Password',
        firstname='Vorname',
        lastname='Nachname',
        email='Email'
    )
    url: str = '/api/config/users/add'
    return render_template('pages/config_users_edit_page.html', default=default, user=user, action_title="Hinzufügen", post_url=url)

@app.route('/api/config/users/edit/', methods=['POST']) # edit user
def config_users_edit():
    try:
        form_data = request.form
        userid: int = int(form_data.get('userid', None))

        user = ConfigurationUsersAPI.get_user(user_id=userid)
        url: str = '/api/config/users/edit/'

        ConfigurationUsersAPI.edit_user(
            userid=userid,
            username=form_data.get('username', None),
            pwd=form_data.get('pwd', None),
            firstname=form_data.get('firstname', None),
            lastname=form_data.get('lastname', None),
            email=form_data.get('email', None),
        )
        return render_template('pages/config_users_edit_page.html', default=default, user=user, action_title="Bearbeiten", post_url=url)
    except:
        resp = Response("invalid request", status=400)
        return resp

# ############################################################ A6 Konfiguration Page Endpoints - USERS \

@app.route('/formular')
def formular_page():
    name = 'Lehrer x'
    return render_template('pages/formular.html', default=default, username=name)


app.run()
