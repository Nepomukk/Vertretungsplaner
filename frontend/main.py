# import inspect
# import os
# import sys

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

import json
import os
from typing import List, TypedDict, Union

import flask
from flask import render_template, request, Response, redirect
from backend.ConfigurationAPI_Roles import ConfigurationAPI_Roles, ConfigurationPages_Roles

# Roles
from backend.ConfigurationManager_Roles import ConfigurationMngrRoles, Roles
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
    'Verwaltung': {
        'name': 'Verwaltung',
        'path': '/config',
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
# ############################################################ A6 Konfiguration Endpoints
@app.route('/config') # get page config
def get_config_page():
    return ConfigurationPages_Roles.get_config_page(default=default)
# ############################################################ A6 Konfiguration Endpoints \
# ############################################################ A6 Konfiguration-roles Endpoints
@app.route('/config/roles') # get page config-roles
def get_config_roles_page():
    return ConfigurationPages_Roles.get_config_roles_page(default=default)

@app.route('/config/roles/add') # get page add role
def config_roles_add_page():    
    return ConfigurationPages_Roles.config_roles_add_page(default=default)

@app.route('/config/roles/edit/<roleid>', methods=['GET']) # get page edit role
def config_roles_edit_page(roleid: str):
    role_id: int = int(roleid)
    return ConfigurationPages_Roles.config_roles_edit_page(default=default, roleid=role_id)

@app.route('/api/config/roles/edit/', methods=['POST']) # edit role
def config_roles_edit():
    try:
        form_data: dict = request.form
        roldeid: int = int(form_data.get('roleid', 0))
        ConfigurationAPI_Roles.config_roles_edit(form_data=form_data, roldeid=roldeid)
        
        return redirect(f'/config/roles/edit/{roldeid}')
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/roles/del/<roleid>', methods=['POST']) # del role
def config_roles_del(roleid: str):
    try:
        role_id: int = int(roleid)

        ConfigurationAPI_Roles.config_roles_del(roleid=role_id)

        return redirect(f'/config/roles')
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/roles/add/', methods=['POST']) # add role
def config_roles_add():
    try:
        form_data = request.form
        roldeid: int = int(form_data.get('roleid', 0))

        ConfigurationAPI_Roles.config_roles_add(form_data=form_data, role_id=roldeid)

        return redirect(f'/config/roles/edit/{roldeid}')
    except:
        resp = Response("invalid request", status=400)
        return resp
# ############################################################ A6 Konfiguration-roles Endpoints \

# ############################################################ A6 Konfiguration-users Endpoints
@app.route('/config/users') # get page config-users
def get_config_users_page():
    users = ConfigurationUsersAPI.get_users_objs()
    url: str = '/api/config/users/del'
    return render_template('pages/config_users_page.html', default=default, users=users, post_url=url)

@app.route('/config/users/edit/<userid>', methods=['GET']) # get page edit users
def config_users_edit_page(userid: str):
    user_id: int = int(userid)
    user = ConfigurationUsersAPI.get_user(user_id=user_id)
    url: str = '/api/config/users/edit/'
    return render_template('pages/config_users_edit_page.html', default=default, user=user, action_title="Bearbeiten", post_url=url)

@app.route('/config/users/add') # get page add user
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

        ConfigurationUsersAPI.edit_user(
            userid=userid,
            username=form_data.get('username', None),
            pwd=form_data.get('pwd', None),
            firstname=form_data.get('firstname', None),
            lastname=form_data.get('lastname', None),
            email=form_data.get('email', None),
        )
        return redirect(f'/config/users/edit/{userid}')
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/users/del/<userid>', methods=['POST']) # del user
def config_users_del(userid: str):
    try:
        user_id: int = int(userid)

        ConfigurationUsersAPI.del_user(userid=user_id)

        return redirect(f'/config/users')
    except:
        resp = Response("invalid request", status=400)
        return resp

@app.route('/api/config/users/add/', methods=['POST']) # add user
def config_users_add():
    try:
        form_data = request.form
        userid: int = int(form_data.get('userid', 0))

        ConfigurationUsersAPI.add_user(
            userid=userid,
            username=form_data.get('username', None),
            pwd=form_data.get('pwd', None),
            firstname=form_data.get('firstname', None),            
            lastname=form_data.get('lastname', None),            
            email=form_data.get('email', None)
        )

        return redirect(f'/config/users/edit/{userid}')
    except:
        resp = Response("invalid request", status=400)
        return resp
# ############################################################ A6 Konfiguration-users Endpoints \

@app.route('/formular')
def formular_page():
    name = 'Lehrer x'
    return render_template('pages/formular.html', default=default, username=name)


app.run()
