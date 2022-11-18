import copy
from os.path import exists

from PyPDF2 import PdfMerger
import os
from pathlib import Path
from datetime import datetime

import flask
import pdfkit as pdfkit
from flask import render_template, redirect, url_for, flash, request, request, make_response, send_file
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_migrate import Migrate
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from werkzeug.security import check_password_hash
from backend.ConfigurationAPI_Roles import ConfigurationAPI_Roles, ConfigurationPages_Roles
from backend.ConfigurationAPI_Users import ConfigurationAPI_Users, ConfigurationPages_Users
from backend.ConfigurationManager_Roles import ConfigurationMngrRoles
from backend.ConfigurationManager_Users import ConfigurationMngrUsers

from database.dbHelper import *
from frontend.forms.loginForm import LoginForm

app = flask.Flask(__name__)
# generated with print(os.urandom(24))
app.secret_key = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"
app.config['SECRET_KEY'] = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"

js_files = os.listdir('static/js')
css_files = os.listdir('static/css')

notifications = [
    {
        'message': 'Der Bereichsleiter hat den Antrag abgelehnt!',
        'path': '/',
    },
    {
        'message': 'Der Bereichsleiter hat den Antrag angenommen!',
        'path': '/',
    },
    {
        'message': 'Der Antrag wurde aktzeptiert!',
        'path': '/',
    },
]

menu_items = {
    'overview': {
        'name': 'Übersicht',
        'path': '/overview',
        'icon': 'fa-solid fa-list-ul',
    },
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
    "notifications": notifications,
}

admin_default = copy.deepcopy(default)
admin_default['menu_items']['manage_users'] = {
    'name': 'Nutzer-Verwaltung',
    'path': '/config/users',
    'icon': 'fa-solid fa-circle-user',
}
admin_default['menu_items']['manage_roles'] = {
    'name': 'Rollen-Verwaltung',
    'path': '/config/roles',
    'icon': 'fa-solid fa-hat-cowboy',
}

# INFO: add hide_menu=True to render_template() to disable the menu for a route

app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:docker@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


def init_db():
    db.drop_all()
    db.create_all()

    db.session.add(Departments('AV Abteilung', 'AV'))
    db.session.add(Departments('Elektrotechnik', 'ET'))
    db.session.add(Departments('IT Abteilung', 'IT'))
    db.session.add(Departments('BFS Abteilung', 'BFS'))
    db.session.add(Departments('ITA Abteilung', 'ITA'))
    db.session.add(Departments('FOS Abteilung', 'FOS'))
    db.session.add(Departments('FS Abteilung', 'FS'))

    db.session.add(AbsenseReasons('Dienstveranstaltung'))
    db.session.add(AbsenseReasons('Prüfungsausschuss'))
    db.session.add(AbsenseReasons('Fortbildung'))
    db.session.add(AbsenseReasons('Unterrichtsgang'))
    db.session.add(AbsenseReasons('Sonstiges'))

    db.session.add(SubstitutionTypes('Fachvertretung'))
    db.session.add(SubstitutionTypes('passive Vertretung'))

    db.session.add(StatusTypes('wartet auf Prüfung', 'bg-info'))
    db.session.add(StatusTypes('wartet auf Korrektur', 'bg-danger'))
    db.session.add(StatusTypes('abgeschlossen', 'bg-success'))

    db.session.add(User("test",  # username
                        "test",  # password
                        "Testania", "Testtosteron", "test@tesstmail.de"))
    db.session.add(Roles("Admin", True, 0))
    db.session.add(Roles("Lehrer", False, 1))
    db.session.add(Roles("Bereichsleiter", False, 2))
    db.session.add(Roles("Vertretungsplaner", False, 3))

    db.session.add(UserToRole(1, 1, 3))
    db.session.add(UserToRole(1, 2, 3))
    db.session.add(UserToRole(1, 3, 3))
    db.session.add(UserToRole(1, 4, 3))

    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=["GET", "POST"])
@app.route('/overview', methods=["GET", "POST"])
@login_required
def home():
    name = ''
    # TODO Filterlogik
    if current_user.is_authenticated:
        name = current_user.firstname + ' ' + current_user.lastname
    user: User = current_user
    is_admin: bool = ConfigurationMngrRoles.is_admin(user_id=user.userid)
    my_default = default
    if is_admin:
        my_default = admin_default
    affected_departments = Departments.query.all()
    absence_reasons = AbsenseReasons.query.all()
    status_types = StatusTypes.query.all()
    form_list = Forms.query.filter(
        Forms.userid == current_user.userid).all()  # TODO Logik erweitern für mehr als die eigenen bzw des Pozesses Rellen des Users benutzen
    formatid_list = []
    dep_list = []
    for form in form_list:
        if form.formatid not in formatid_list:
            formatid_list.append(form.formatid)
            dep_list.append(FromatToDepartment.query.filter(FromatToDepartment.formatid == form.formatid).all())
    depart_dict = {}
    for form in form_list:
        temp_short_list = []
        for temp_list in dep_list:
            for temp_dep in temp_list:
                if temp_dep.formatid == form.formatid:
                    for department in affected_departments:
                        if temp_dep.departmentid == department.id:
                            temp_short_list.append(department.shortcut)
        depart_dict[str(form.formatid)] = temp_short_list

    return render_template('pages/overview.html', default=default, username=name, departments=affected_departments,
                           absence_reasons=absence_reasons, status_types=status_types, form_list=form_list,
                           dep_dict=depart_dict)


@app.route('/login', methods=["GET", "POST"])
def login():
    # to reset the database restore Default or update structure
    # init_db()
    # db.drop_all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.pwd, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Login ist fehlgeschlagen, Benutzername oder Passwort ist nicht korrekt.')
        else:
            flash('Der Benutzer existiert nicht')
    return render_template('pages/A1-login-page.html', default=default, form=form, hide_menu=True)


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/formular', methods=["GET", "POST"])
@login_required
def formular_page():
    name = ''
    if current_user.is_authenticated:
        name = current_user.firstname + ' ' + current_user.lastname
    user: User = current_user
    is_admin: bool = ConfigurationMngrRoles.is_admin(user_id=user.userid)
    my_default = default
    if is_admin:
        my_default = admin_default

    if flask.request.method == 'GET':
        users = User.query.filter(User.userid != current_user.userid).all()
        absence_reasons = AbsenseReasons.query.all()
        affected_departments = Departments.query.all()
        raw_formatid = request.args.get('formatid')
        allow_comment = False
        allow_edit = True
        form = None
        lessons = None
        modus = 1  # create
        if raw_formatid is not None and raw_formatid != '' and raw_formatid.isdigit():
            formatid = int(raw_formatid)
            form = Forms.query.get(formatid)
            lessons = SubLessons.query.filter_by(formatid=formatid).all()
            if form is None:
                return redirect(url_for('home'))

            if form.status == 3 or form.activ is False:
                allow_edit = False
                modus = 3  # show
            elif form.userid is not current_user.userid:
                allow_edit = False
                allow_comment = True
                modus = 4  # accept
            elif form.userid == current_user.userid:
                modus = 2  # Update

        return render_template('pages/formular.html', default=my_default, username=name,
                               absence_reasons=absence_reasons,
                               affected_departments=affected_departments, allow_comment=allow_comment,
                               allow_edit=allow_edit, users=users, form=form, lessons=lessons, modus=modus)
    elif flask.request.method == 'POST':
        modus = int(request.args.get('modus'))
        if modus is None or modus == 1:
            formatid = 0
            form = Forms(current_user.userid,
                         request.form['absence-reasons'],
                         request.form['other'],
                         request.form['affected-departments'],
                         1,
                         None,
                         True,
                         datetime.now().date()
                         )

            with app.app_context():
                db.session.add(form)
                db.session.flush()
                db.session.commit()
                formatid = form.formatid

            saveAppendFile(form, request)

            for department in zip(request.form.getlist('affected-departments')):
                with app.app_context():
                    db.session.add(FromatToDepartment(formatid=formatid, departmentid=department))
                    db.session.commit()

            for date, std_from, std_to, subject, subclass, subteacher, subcontent in zip(request.form.getlist('date'),
                                                                                         request.form.getlist(
                                                                                             'std_from'),
                                                                                         request.form.getlist(
                                                                                             'std_to'),
                                                                                         request.form.getlist(
                                                                                             'subject'),
                                                                                         request.form.getlist(
                                                                                             'subclass'),
                                                                                         request.form.getlist(
                                                                                             'subteacher'),
                                                                                         request.form.getlist(
                                                                                             'subcontent')):
                with app.app_context():
                    temp_lesson = SubLessons(formatid,
                                             int(std_from),
                                             int(std_to),
                                             subject,
                                             subclass,
                                             None,
                                             subteacher,
                                             current_user.userid,
                                             datetime.now().date(),
                                             subcontent,
                                             datetime.strptime(date, '%Y-%m-%d').date()
                                             )
                    db.session.add(temp_lesson)
                    db.session.commit()
        elif modus == 2:
            formatid = request.form.get('formatid_btn')
            form = Forms.query.get(formatid)

            saveAppendFile(form, request)

            with app.app_context():
                FromatToDepartment.query.filter_by(formatid=formatid).delete()
                SubLessons.query.filter_by(formatid=formatid).delete()
                if form.absensereasons != int(request.form['absence-reasons']):
                    form.absensereasons = int(request.form['absence-reasons'])
                if form.other != request.form['other']:
                    form.other = request.form['other']
                if form.workarea != int(request.form['affected-departments']):
                    form.workarea = int(request.form['affected-departments'])
                form.status = 1
                db.session.commit()

            for department in zip(request.form.getlist('affected-departments')):
                with app.app_context():
                    db.session.add(FromatToDepartment(formatid=formatid, departmentid=department))
                    db.session.commit()

            for date, std_from, std_to, subject, subclass, subteacher, subcontent in zip(request.form.getlist('date'),
                                                                                         request.form.getlist(
                                                                                             'std_from'),
                                                                                         request.form.getlist(
                                                                                             'std_to'),
                                                                                         request.form.getlist(
                                                                                             'subject'),
                                                                                         request.form.getlist(
                                                                                             'subclass'),
                                                                                         request.form.getlist(
                                                                                             'subteacher'),
                                                                                         request.form.getlist(
                                                                                             'subcontent')):
                temp_lesson = SubLessons(formatid,
                                         int(std_from),
                                         int(std_to),
                                         subject,
                                         subclass,
                                         None,
                                         subteacher,
                                         current_user.userid,
                                         datetime.now().date(),
                                         subcontent,
                                         datetime.strptime(date, '%Y-%m-%d').date()
                                         )
                with app.app_context():
                    db.session.add(temp_lesson)
                    db.session.commit()
        elif modus == 4:
            button_string = ''
            action = True
            end_form = False
            if request.form.get('accept_btn') is not None:
                button_string = request.form.get('accept_btn')
            else:
                button_string = request.form.get('decline_btn')

            if button_string.split('_')[0] == 'not':
                action = False

            formatid = int(button_string.split('_')[1])

            with app.app_context():
                confirmations = Confirmation.query.filter_by(formatid=formatid).order_by(Confirmation.id).all()
                user_roles = UserToRole.query.filter_by(userid=current_user.userid).all()
                cnt_roles = Roles.query.filter_by(admin=False).count() - 1
                cnt_confirmations = 1
                for confirmation in confirmations:
                    if confirmation.ok:
                        cnt_confirmations += 1
                    else:
                        cnt_confirmations = 0
                if cnt_roles >= cnt_confirmations:
                    cnt_confirmations += 1
                    act_role = Roles.query.filter_by(admin=False, level=cnt_confirmations).first()
                    for user_role in user_roles:
                        if user_role.roleid == act_role.roleid:
                            if action and (cnt_roles + 1) == act_role.level:
                                end_form = True
                            confirmation = Confirmation(current_user.userid, formatid, datetime.now().date(), action)
                            db.session.add(confirmation)
                db.session.commit()

            with app.app_context():
                form = Forms.query.get(formatid)
                if form.fcomment != request.form['fcomment']:
                    form.fcomment = request.form['fcomment']
                if end_form:
                    form.status = 3
                    form.activ = False
                if action is not True:
                    form.status = 2
                db.session.commit()
    return redirect(url_for('home'))


@app.route('/formular/pdf', methods=["GET"])
@login_required
def formular_pdf():
    if flask.request.method == 'GET':
        raw_formatid = request.args.get('formatid')
        if raw_formatid is not None and raw_formatid.isdigit():
            merger = PdfMerger()
            img = Path("static/img/logo.png").absolute()
            formatid = int(raw_formatid)
            form = Forms.query.filter_by(formatid=formatid).first()
            lessons = SubLessons.query.filter_by(formatid=formatid).order_by(SubLessons.lessondate).all()
            date = lessons[0].lessondate.strftime("%d.%m.%Y") + '-' + lessons[1].lessondate.strftime("%d.%m.%Y")
            # render Template
            html = render_template(
                "pdflayout/pdf.html",
                default=default, form=form, lessons=lessons, date=date, img=img, hide_menu=True)
            Path("files/requests").mkdir(parents=True, exist_ok=True)
            file_path = "files/requests/Request_" + str(form.formatid) + ".pdf"
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(html, file_path, configuration=config)
            append_file = 'files/appends/Appendix_' + str(form.formatid) + ".pdf"
            file_path_end = "files/combine/Request_" + str(form.formatid) + "_combined.pdf"
            if exists(append_file):
                merger.append(file_path)
                merger.append(append_file)
                merger.write(file_path_end)
                merger.close()
                return send_file(file_path_end, as_attachment=True)
            return send_file(file_path, as_attachment=True)


@app.route('/password-reset')
def password_reset():
    kontakt_str = ''
    with app.app_context():
        adimn_role = Roles.query.filter_by(admin=True).first()
        admin_id = UserToRole.query.filter_by(roleid=adimn_role.roleid).first()
        admin = User.query.get(admin_id.userid)
        kontakt_str = 'Bitte kontaktieren Sie den Admin mit dieser E-Mail-Adresse: ' + admin.email + '.'
    error = {
        'error_title': 'Passwort vergessen?',
        'error_text': kontakt_str,
    }
    return render_template('pages/error.html', hide_menu=True, default=default, error=error)


def saveAppendFile(form, request):
    if request.files['addfile'].filename != '':
        f = request.files['addfile']
        f.save('files/appends/Appendix_' + str(form.formatid) + ".pdf")


@app.errorhandler(404)
def page_not_found(e):
    hide_menu = True
    error = {
        'error_title': 'Seite nicht gefunden!',
        'error_text': 'Tut uns Leid, diese Seite ist leider nicht verfügbar.',
    }
    if current_user.is_authenticated and current_user.username is not None:
        hide_menu = False
    return render_template("pages/error.html", hide_menu=hide_menu, default=default, error=error), 404


# ############################################################ A6 Konfiguration Endpoints
@app.route('/config') # get page config
@login_required
def get_config_page():
    user: User = current_user
    is_admin: bool = ConfigurationMngrRoles.is_admin(user_id=user.userid)
    if not is_admin:
        redirect(url_for('login'))
    return ConfigurationPages_Roles.get_config_page(default=admin_default)
# ############################################################ A6 Konfiguration Endpoints \
# ############################################################ A6 Konfiguration-roles Endpoints
@app.route('/config/roles') # get page config-roles
def get_config_roles_page():
    return ConfigurationPages_Roles.get_config_roles_page(default=admin_default)

@app.route('/config/roles/add') # get page add role
def config_roles_add_page():
    return ConfigurationPages_Roles.config_roles_add_page(default=admin_default)

@app.route('/config/roles/edit/<roleid>', methods=['GET']) # get page edit role
def config_roles_edit_page(roleid: str):
    role_id: int = int(roleid)
    return ConfigurationPages_Roles.config_roles_edit_page(default=admin_default, roleid=role_id)

@app.route('/api/config/roles/edit/', methods=['POST']) # edit role
def config_roles_edit():
    return ConfigurationAPI_Roles.config_roles_edit(form_data=request.form)

@app.route('/api/config/roles/del/<roleid>', methods=['POST']) # del role
def config_roles_del(roleid: str):
    return ConfigurationAPI_Roles.config_roles_del(roleid=roleid)

@app.route('/api/config/roles/add', methods=['POST']) # add role
def config_roles_add():
    return ConfigurationAPI_Roles.config_roles_add(form_data=request.form)
# ############################################################ A6 Konfiguration-roles Endpoints \

# ############################################################ A6 Konfiguration-users Endpoints
@app.route('/config/users') # get page config-users
def get_config_users_page():
    return ConfigurationPages_Users.get_config_users_page(default=admin_default)

@app.route('/config/users/edit/<userid>', methods=['GET']) # get page edit users
def config_users_edit_page(userid: str):
    return ConfigurationPages_Users.config_users_edit_page(userid=userid, default=admin_default)

@app.route('/config/users/add') # get page add user
def config_users_add_page():
    return ConfigurationPages_Users.config_users_add_page(default=admin_default)

@app.route('/api/config/users/edit/', methods=['POST']) # edit user
def config_users_edit():
    return ConfigurationAPI_Users.config_users_edit(form_data=request.form)

@app.route('/api/config/users/del/<userid>', methods=['POST']) # del user
def config_users_del(userid: str):
    return  ConfigurationAPI_Users.config_users_del(userid=userid)

@app.route('/api/config/users/add', methods=['POST']) # add user
def config_users_add():
    return ConfigurationAPI_Users.config_users_add(form_data=request.form)
# ############################################################ A6 Konfiguration-users Endpoints \


if __name__ == "__main__":
    app.run()
