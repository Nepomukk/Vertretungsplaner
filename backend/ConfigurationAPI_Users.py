
from flask import render_template, Response, redirect
from backend.ConfigurationManager_Users import ConfigurationMngrUsers
from database.users import User

class ConfigurationPages_Users:
    def get_config_users_page(default):
        users = ConfigurationMngrUsers.get_users_objs()
        url: str = '/api/config/users/del'
        return render_template('pages/config_users_page.html', default=default, users=users, post_url=url)

    def config_users_edit_page(userid: str, default):
        user_id: int = int(userid)
        user = ConfigurationMngrUsers.get_user(user_id=user_id)
        url: str = '/api/config/users/edit/'
        return render_template('pages/config_users_edit_page.html', default=default, user=user, action_title="Bearbeiten", post_url=url)

    def config_users_add_page(default):
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


class ConfigurationAPI_Users:
    def config_users_edit(form_data: dict):
        try:
            userid: int = int(form_data.get('userid', None))

            ConfigurationMngrUsers.edit_user(
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

    def config_users_del(userid: str):
        try:
            user_id: int = int(userid)

            ConfigurationMngrUsers.del_user(userid=user_id)

            return redirect(f'/config/users')
        except:
            resp = Response("invalid request", status=400)
            return resp

    def config_users_add(form_data: dict):
        try:
            userid: int = int(form_data.get('userid', 0))

            ConfigurationMngrUsers.add_user(
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