#! /usr/bin/env python

__author__ = 'wilson.sumanang@gmail.com'

# External Imports
import os
from flask import Flask, render_template, session, flash

# Internal Imports
from app.account import account
from app.media import media
from app.views import views
from photodl.settings import get_config

app_dir = os.path.dirname(os.path.realpath(__file__))


def create_flask_app():
    app = Flask(__name__)

    server_settings = get_config(app_dir, 'photodl')
    app.config['server_settings'] = server_settings
    app.config.update(**server_settings.flask_config)

    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(views, url_prefix='/views')
    app.register_blueprint(media, url_prefix='/media')

    @app.route('/')
    @app.route('/index')
    def index():
        if 'access_token' in session:
            flash('you are already signed-in')
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
