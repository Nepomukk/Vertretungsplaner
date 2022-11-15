import json
import os

import flask
from flask import request, jsonify
from flask import render_template

# Roles
from backend.model import Role, User

# my imports
from typing import List, Union, TypedDict
from backend import Configuration_Roles

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# load all file names from the respective folder to automatically add all files within
js_files = os.listdir('frontend/static/js')
css_files = os.listdir('frontend/static/css')
# add to default var set for all templates
default = {
    "js_files": js_files,
    "css_files": css_files,
}
##### BeisplielDATEN
placeholder_roles: List[Role] = [
    Role("user-1", 1, False),
    Role("user-2", 1, False),
    Role("user-3", 1, False)
]



@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', default=default, username=name)

# A6 Konfiguration Endpoints
@app.route('/configuration/roles') # Manage roles
def config_roles():
    role_dicts: List[Role.RoleSchema] = Configuration_Roles.ConfigurationRoles.get_roles_dicts()
    return render_template('pages/configuration_roles.html', default=default, roles = role_dicts)

@app.route('/configuration/role_edit') # Edit Role
def config_edit_role():
    role_id: int = 1 # get this
    return render_template('pages/configuration_edit_role.html', default=default, role_id=role_id)

@app.route('/configuration/users') # Manage users
def config_users():
    return render_template('pages/configuration_users.html', default=default)

@app.route('/configuration/user_edit') # Edit user
def config_edit__user():
    user_id: int = 1 # get this
    return render_template('pages/configuration_edit_role.html', default=default, user_id=user_id)

app.run()
