import json
import flask
from flask import request, jsonify
from flask import render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    name = 'Lehrer x'
    return render_template('pages/home.html', username=name)


app.run()
