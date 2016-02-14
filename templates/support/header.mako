<%page args="title"/>\
<%! from flask import request, url_for %>\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>${title}</title>
        <link rel="stylesheet" href="${request.script_root}${url_for('static', file='style.css')}" type="text/css" />
    </head>
    <body>
        <header>
            <h1><a href="${request.script_root}">TIF Calculator</a></h1>
            <p>Calculate the <a href="https://en.wikipedia.org/wiki/User:The_Earwig/Sandbox/TIF">template influence factor</a> of any page on the English Wikipedia.</p>
        </header>
        <div id="container">
