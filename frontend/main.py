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
from flask import jsonify, render_template, request

# Roles
from backend.Configuration_Roles import ConfigurationRolesAPI
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

# A6 Konfiguration Page Endpoints
@app.route('/config/roles') # get page config-roles
def get_config_roles_page():
    roles = ConfigurationRolesAPI.get_roles_objs()
    return render_template('pages/config_roles_page.html', default=default, roles=roles)

@app.route('/api/config/roles/del/<roleid>', methods=['GET']) # del role
def config_roles_del(roleid: int):
    roles = ConfigurationRolesAPI.get_roles_objs()

    ConfigurationRolesAPI.del_role(roleid=roleid)
    return render_template('pages/config_roles_page.html', default=default, roles=roles)

@app.route('/api/config/roles/add/') # add role
def config_roles_add():
    pass

@app.route('/api/config/roles/edit/<roleid>', methods=['GET']) # edit role
def config_roles_edit(roleid: int):
    roleid: int = 1
    name: str
    admin: bool
    level: int
    return render_template('pages/configuration_edit_role.html', default=default, role_id=roleid)


# @app.route('/api/config/users/') # get page config-roles
# def get_config_users_page():
#     pass

# @app.route('/api/config/users/edit/') # edit user
# def config_edit_user():
#     pass

# @app.route('/api/config/users/add/') # edit user
# def config_add_user():
#     pass

@app.route('/formular')
def formular_page():
    name = 'Lehrer x'
    return render_template('pages/formular.html', default=default, username=name)


app.run()
