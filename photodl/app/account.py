#! /usr/bin/env python

# External Imports
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    render_template,
    session,
    flash
)
from functools import wraps
from instagram import client
from instagram.oauth2 import OAuth2AuthExchangeError

api = None


class AccountBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global api
        api = client.InstagramAPI(**app.config['server_settings'].instagram)

        super(AccountBlueprint,
              self).register(app, options, first_registration)

account = AccountBlueprint('account', __name__)


def instagram_login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        access_token = session.get('access_token', None)
        if not access_token:
            return redirect(url_for('account.login'))
        else:
            return f(*args, **kwargs)
    return decorator


@account.route('/')
@account.route('/login')
def login():
    scope = ['basic', 'comments', 'relationships', 'likes']
    url = api.get_authorize_url(scope=scope)
    return redirect(url)


@account.route('/logout')
def logout():
    del session['access_token']
    del session['user']
    return render_template('index.html')


@account.route('/oauth2_callback')
def oauth2_callback():
    request_code = request.args.get('code')
    if not request_code:
        flash('missing request code from instagram')
        return redirect(url_for('index'))
    try:
        access_token, user_info = \
            api.exchange_code_for_access_token(request_code)
    except OAuth2AuthExchangeError:
        flash('Could not login to instagram')
        return redirect(url_for('index'))

    if not access_token:
        flash('could not get access token')
        return redirect(url_for('index'))
    session['access_token'] = access_token
    session['user'] = user_info
    print access_token
    flash('You are now logged in using instagram oauth')
    return redirect(url_for('index'))
