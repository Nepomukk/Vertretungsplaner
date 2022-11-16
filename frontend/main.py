import json
import os

import flask
from flask import request, jsonify
from flask import render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# load all file names from the respective folder to automatically add all files within
js_files = os.listdir('static/js')
css_files = os.listdir('static/css')
# add to default var set for all templates
default = {
    "js_files": js_files,
    "css_files": css_files,
}


@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', default=default, username=name)


@app.route('/login')
def loginpage():
    username = 'User X'
    return render_template('pages/A1-login-page.html', default=default, username=username)


# Invalid URL

#TODO für eingeloggte User muss das Menü wieder angezeigt werden
@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/error.html",hide_menu=True, default=default), 404



app.run()
