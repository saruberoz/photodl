#! /usr/bin/env python

__author__ = 'wilson.sumanang@gmail.com'

# External Imports
from flask import Flask, render_template, request, session, redirect, url_for, flash

# Internal Imports
from app.views import views
from app.account import account


def create_flask_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(views, url_prefix='/views')

    # @app.before_request
    # def before_request():
    #     if 'access_token' not in session:
    #         # session['access_token'] = None
    #         return redirect(url_for('account.login'))

    # @app.teardown_request
    # def teardown_request(exception):
    #     print 'teardown request'

    @app.route('/')
    @app.route('/index')
    def index():
        if 'access_token' not in session:
            return render_template('index.html')
        flash('you are already signed-in')
        return redirect(url_for('views.get_user_photos'))

    @app.errorhandler(404)
    def page_not_found(error):
        return  render_template('404.html'), 404

    # @app.errorhandler(Exception)
    # def exception_handler(error):
    #     return Exception

    return app
