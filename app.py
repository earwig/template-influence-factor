#! /usr/bin/env python
# -*- coding: utf-8  -*-

from flask import Flask, g
from flask.ext.mako import MakoTemplates, render_template

from tif.util import catch_errors, set_up_hash_caching

app = Flask(__name__)
MakoTemplates(app)
set_up_hash_caching(app)

@app.before_request
def prepare_request():
    g._db = None

@app.teardown_appcontext
def close_databases(error):
    if g._db:
        g._db.close()

@app.route("/")
@catch_errors(app)
def index():
    return render_template("index.mako")

if __name__ == '__main__':
    app.run()
