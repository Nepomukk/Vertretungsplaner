import json
import os

import flask
from flask import request, jsonify
from flask import render_template

app = flask.Flask(__name__)


# app.config["DEBUG"] = True

@app.route('/')
def home():
    pass


app.run()
