import json
import flask
from flask import request, jsonify
from flask import render_template


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
@app.route('/index')
def index():
    name = 'Rosalia'
    return render_template('home.html', username=name)


app.run()
