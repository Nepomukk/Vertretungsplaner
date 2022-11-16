import json
import os

import flask
from flask import request, jsonify
from flask import render_template

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# load all file names from the respective folder to automatically add all files within
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


@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', default=default, username=name)


@app.route('/formular')
def formular_page():
    name = 'Lehrer x'
    allow_comment = True
    allow_edit = True
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
                           absence_reasons=absence_reasons, affected_departments=affected_departments, allow_comment= allow_comment,
                           allow_edit=False)

app.run()
