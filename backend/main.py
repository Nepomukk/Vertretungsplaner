#
# import flask
# from flask import request, session, redirect, make_response, g
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
#
# import database.dbHelper as dbClasses
#
# app = flask.Flask(__name__)
# # generated with print(os.urandom(24))
# app.secret_key = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"
# app.config['SECRET_KEY'] = "mt\xd2\xa5M_\xc5\xc3\r\xf3\x1b\xd4R\xce\xa3\xb8\xa2!?:\xeb\xaa\xc9\x8b\xf2m"
#
# app.config["DEBUG"] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:docker@localhost:5432/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
#
# @login_manager.user_loader
# def load_user():
#
#
# @app.before_request
# def before_request():
#     if 'user_id' in session:
#         sess = dbClasses.Session.getSession()
#         with sess() as con_session:
#             login_user = con_session.query(dbClasses.User).filter(dbClasses.User.userid == session['user_id']).first()
#             g.user = login_user
#
#
# @app.route('/api/login', methods=["POST"])
# def login():
#     session.pop('user_id', None)
#     dic_request = request.json
#     username = dic_request['username']
#     password = dic_request['password']
#
#     sess = dbClasses.Session.getSession()
#     with sess() as con_session:
#         login_user = con_session.query(dbClasses.User).filter(dbClasses.User.username == username, dbClasses.User.pwd == password).first()
#         if login_user is not None:
#             session['user_id'] = login_user.userid
#             return redirect('/formular')
#     return make_response('Login ist fehlgeschlagen', 401)
#
#
# @app.route('/api/logout', methods=["POST"])
# def logout():
#     session.pop(request.json['username'])
#     g.user = None
#     return redirect('/login')
#
#
#     app.run()
