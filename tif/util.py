# -*- coding: utf-8  -*-

from functools import wraps
from hashlib import md5
from os import path
from traceback import format_exc

from flask.ext.mako import render_template, TemplateError

__all__ = ["catch_errors", "set_up_hash_caching"]

def catch_errors(app):
    def callback(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TemplateError as exc:
                app.logger.error(u"Caught exception:\n{0}".format(exc.text))
                return render_template("error.mako", traceback=exc.text)
            except Exception:
                app.logger.exception(u"Caught exception:")
                return render_template("error.mako", traceback=format_exc())
        return inner
    return callback

def set_up_hash_caching(app):
    def callback(app, error, endpoint, values):
        if endpoint == "static" and "file" in values:
            fpath = path.join(app.static_folder, values["file"])
            mtime = path.getmtime(fpath)
            cache = app._hash_cache.get(fpath)
            if cache and cache[0] == mtime:
                hashstr = cache[1]
            else:
                with open(fpath, "rb") as f:
                    hashstr = md5(f.read()).hexdigest()
                app._hash_cache[fpath] = (mtime, hashstr)
            return "/static/{0}?v={1}".format(values["file"], hashstr)
        raise error

    app._hash_cache = {}
    app.url_build_error_handlers.append(lambda *args: callback(app, *args))
