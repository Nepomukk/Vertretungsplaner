import base64
import os
from pathlib import Path

import flask
import pdfkit as pdfkit
from flask import render_template, redirect, url_for, flash, request, make_response, send_file
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

from database.dbHelper import *
from frontend.forms.loginForm import LoginForm

app = flask.Flask(__name__)
# generated with print(os.urandom(24))
app.secret_key = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"
app.config['SECRET_KEY'] = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"

js_files = os.listdir('static/js')
css_files = os.listdir('static/css')

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

    db.session.add(StatusTypes('erstellt'))
    db.session.add(StatusTypes('bearbeiten fertig gestellt'))
    db.session.add(StatusTypes('abgelehnt von Bereichsleiter'))
    db.session.add(StatusTypes('angenommen von Bereichsleiter'))
    db.session.add(StatusTypes('abgelehnt von Vertretungsplaner'))
    db.session.add(StatusTypes('angenommen von Vertretungsplaner'))

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


@app.route('/')
@login_required
def home():
    name = ''
    if current_user.is_authenticated:
        name = current_user.firstname + ' ' + current_user.lastname
    return render_template('pages/home.html', default=default, username=name)


@app.route('/login', methods=["GET", "POST"])
def login():
    # to reset the database restore Default or update structure
    # init_db()
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


@app.route('/formular')
@login_required
def formular_page():
    name = ''
    if current_user.is_authenticated:
        name = current_user.firstname + ' ' + current_user.lastname
    absence_reasons = {
        'work_event': {
            'name': 'Dienstveranstaltung',
            'enable_textarea': False,
        },
        'exma_committee': {
            'name': 'Prüfungsausschuss',
            'enable_textarea': False,
        },
        'further_education': {
            'name': 'Fortbildung',
            'enable_textarea': False,
        },
        'lesson_course': {
            'name': 'Unterrichtsgang',
            'enable_textarea': False,
        },
        'other': {
            'name': 'Sonstiges',
            'enable_textarea': True,
        },
    }
    affected_departments = {
        'av': {
            'name': 'AV',
        },
        'et': {
            'name': 'ET',
        },
        'it': {
            'name': 'IT',
        },
    }
    return render_template('pages/formular.html', default=default, username=name,
                           absence_reasons=absence_reasons,
                           affected_departments=affected_departments)


@app.route('/formular/pdf', methods=["GET", "POST"])
@login_required
def formular_pdf():
    if flask.request.method == 'GET':
        raw_formatid = request.args.get('formatid')
        if raw_formatid is not None and raw_formatid.isdigit():
            img = Path("static/img/logo.png").absolute()
            formatid = int(raw_formatid)
            form = Forms.query.filter_by(formatid=formatid).first()
            lessons = SubLessons.query.filter_by(formatid=formatid).order_by(SubLessons.lessondate).all()
            date = lessons[0].lessondate.strftime("%d.%m.%Y") + '-' + lessons[1].lessondate.strftime("%d.%m.%Y")
            # render Template
            html = render_template(
                "pdflayout/pdf.html",
                default=default, form=form, lessons=lessons, date=date, img=img, hide_menu=True)
            Path("requests").mkdir(parents=True, exist_ok=True)
            file_path = "requests/Request_" + str(form.formatid) + ".pdf"
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(html, file_path, configuration=config)
            return send_file(file_path, as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    hide_menu = True
    if current_user.is_authenticated and current_user.username is not None:
        hide_menu = False
    return render_template("pages/error.html", hide_menu=hide_menu, default=default), 404


if __name__ == "__main__":
    app.run()
