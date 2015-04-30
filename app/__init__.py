# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, url_for
from flask.ext.cache import Cache
from py2neo import neo4j, authenticate
from logging.handlers import RotatingFileHandler
import logging

from app.models.utils import Utils

app = Flask(__name__)
app.config.from_object('config')

app.jinja_env.filters['datetimeformat'] = Utils.format_datetime
app.jinja_env.filters['formatunix'] = Utils.from_unix
app.jinja_env.filters['utf'] = Utils.to_utf8

authenticate(app.config['NEO4J_HOST'], app.config['NEO4J_USER'], app.config['NEO4J_PASS'])
db = neo4j.Graph("http://{0}/db/data".format(app.config['NEO4J_HOST']))
cache = Cache(app=app, config={'CACHE_TYPE': 'simple'})

handler = RotatingFileHandler(app.config['LOGFILE'], maxBytes=4096000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


# error handlers
@app.errorhandler(403)
def error_403(e):
    return render_template('errors/error_403.html'), 403


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/error_404.html'), 404


@app.errorhandler(410)
def error_410(e):
    return render_template('errors/error_410.html'), 410


@app.errorhandler(500)
def error_500(e):
    return render_template('errors/error_500.html'), 500


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser (and rules that require parameters)
        if "GET" in rule.methods and Utils.no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    return jsonify(links)

from app.controllers.exampleController import Example
app.register_blueprint(Example, url_prefix='/example')


app.logger.info("[INFO] App initialized!")