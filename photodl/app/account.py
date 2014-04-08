#! /usr/bin/env python

# External Imports
import requests
from flask import Blueprint, request, url_for, redirect, g, jsonify, render_template, session, flash
from instagram import client
from instagram.oauth2 import OAuth2AuthExchangeError


CONFIG = {
    'client_id': 'ea2ea54c662c4a8ba136adb5e2c25a7a',
    'client_secret': '6ba5cd189f114dc9975596a10b2f76f0',
    'redirect_uri' : 'http://localhost:5001/account/oauth2_callback'
    # 'redirect_uri': 'http://photodl.herokuapp.com/'
}

api = client.InstagramAPI(**CONFIG)

account = Blueprint('account', __name__)

@account.route('/')
@account.route('/login')
def login():
    scope = ['basic', 'comments', 'relationships', 'likes']
    url = api.get_authorize_url(scope=scope)
    # return '<a href="%s">Connect with Instagram</a>' % url
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
        return 'Missing request_code from instagram', 400
    try:
        access_token, user_info = api.exchange_code_for_access_token(request_code)
    except OAuth2AuthExchangeError:
        flash('Could not login to instagram')
        return render_template('index.html')
        # return 'Could not login to instagram <br/>Click <a href="/account/login"> here </a> to retry the login process.'

    if not access_token:
        return 'could not get access token', 200
    session['access_token'] = access_token
    session['user'] = user_info
    print access_token
    flash('You are now logged in using instagram oauth')
    return redirect(url_for('views.get_user_photos'))
    # return 'Your access token is %s.<br/>Click <a href="/views/download_photos">here</a> to download your photos may take a while.' % (access_token)
