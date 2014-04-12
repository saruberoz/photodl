#! /usr/bin/env python

# External Imports
import json
import requests
from flask import Blueprint, request, jsonify, render_template, session

# Internal Imports
from account import instagram_login_required

MAX_COUNT = 30

views = Blueprint('views', __name__)


@views.route('/media_by_hashtag')
@instagram_login_required
def get_media_by_hashtag():
    hashtag = request.args.get('hashtag', 'bunny')
    url = 'https://api.instagram.com/v1/tags/' \
        '{hashtag}/media/recent?access_token={access_token}'.format(
            hashtag=hashtag, access_token=session['access_token'])
    response = requests.get(url)
    templateData = {
        'data': response.text
    }
    return render_template('json.html', **templateData)


@views.route('/followed_by')
@instagram_login_required
def get_user_followed_by():
    json_data = request.args.get('json', False)
    url = 'https://api.instagram.com/v1/users/3/followed-by' \
        '?access_token={access_token}'.format(
            access_token=session['access_token'])
    response = requests.get(url)
    if json_data:
        return jsonify(data=json.loads(response.text))
    return render_template('json.html', data=response.text)


@views.route('/get_user_info')
@instagram_login_required
def get_instagram_user_info():
    username = request.args.get('username', 'bunnymama')

    url = 'https://api.instagram.com/v1/users/search' \
        '?q={username}&count=1&access_token={access_token}'.format(
            username=username, access_token=session['access_token'])
    response = requests.get(url)
    data = json.loads(response.text)

    templateData = {
        'username': username,
        'user_id': data['data'][0]['id'],
        'full_name': data['data'][0]['full_name'],
        'profile_picture': data['data'][0]['profile_picture'],
        'bio': data['data'][0]['bio']
    }
    return render_template('user.html', **templateData)
