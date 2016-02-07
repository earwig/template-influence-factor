This is a tool that calculates the
[Template Influence Factor](https://en.wikipedia.org/wiki/User:The_Earwig/Sandbox/TIF)
of a [Wikipedia template](https://en.wikipedia.org/wiki/Help:Template), which
is a measure of how
[high risk](https://en.wikipedia.org/wiki/Wikipedia:High-risk_templates) it is,
for the purposes of anti-vandalism. It runs on
[Wikimedia Labs](https://tools.wmflabs.org/earwig-dev/tif).

Dependencies
============

* [earwigbot](https://github.com/earwig/earwigbot) >= 0.2
* [flask](http://flask.pocoo.org/) >= 0.10.1
* [flask-mako](https://pythonhosted.org/Flask-Mako/) >= 0.3
* [mako](http://www.makotemplates.org/) >= 1.0.3
* [oursql](http://packages.python.org/oursql/) >= 0.9.3.1

Running
=======

- Install all dependencies listed above.

- Create an SQL database ...

- Create an earwigbot instance in `.earwigbot` (run `earwigbot .earwigbot`). In
  `.earwigbot/config.yml`, fill out the connection info for the database by
  adding the following to the `wiki` section:

        _tifSQL:
            host: <hostname of database server>
            db:   <name of database>

  If additional arguments are needed by `oursql.connect()`, like usernames or
  passwords, they should be added to the `_tifSQL` section.

- Start the web server (on Tool Labs, `webservice2 uwsgi-python start`).
