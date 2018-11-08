from flask import Flask, render_template, redirect, url_for, request
from werkzeug.debug import DebuggedApplication
from config import ConfigPicker
import os

conf = ConfigPicker(os.environ['ENV'])

# app = Flask(__name__)
# app.config.from_object(conf)


def create_app():
    # Insert whatever else you do in your Flask app factory.

    app = Flask(__name__)
    app.config.from_object(conf)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


app = create_app()

