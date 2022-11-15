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

menu_items = {
    'formular': {
        'name': 'Formular erstellen',
        'path': '/formular',
    },
}

# add to default var set for all templates
default = {
    "js_files": js_files,
    "css_files": css_files,
    "menu_items": menu_items,
}


@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', default=default, username=name)


@app.route('/formular')
def formular_page():
    name = 'Lehrer x'
    return render_template('pages/formular.html', default=default, username=name)


@app.route('/notifications')
def test_message_bell():
    messages = []
    username = 'Lehrer X'
    message1 = "Hallo" + username
    message2 = "Antrag angenommen"
    messages.append(message1)
    messages.append(message2)
    # wird später mit for-Schleife aus der DB umgesetzt"
    return render_template('pages/layout.html', messages=messages)

app.run()
