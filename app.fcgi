#! /data/project/earwig-dev/env/bin/python
# -*- coding: utf-8  -*-

from flask import Flask, request
from flask.ext.mako import MakoTemplates, render_template

from tif.calc import calculate_tif
from tif.util import catch_errors, set_up_hash_caching

app = Flask(__name__)
MakoTemplates(app)
set_up_hash_caching(app)

@app.route("/")
@catch_errors(app)
def index():
    title = request.args.get("title")
    result = calculate_tif(title) if title else {}
    return render_template("index.mako", result=result)

if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
