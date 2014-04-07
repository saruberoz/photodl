#! /usr/bin/env python

# External Imports
import requests
import urllib
from flask import Blueprint, request, redirect, jsonify, render_template, url_for, session
from instagram.client import InstagramAPI


views = Blueprint('views', __name__)

@views.route('/get_user_id')
def get_instagram_user_id():
    if 'access_token' not in session:
        return redirect(url_for('account.login'))
    user_name=request.args.get('user_name')

    url = 'https://api.instagram.com/v1/users/search?q={user_name}&count=1&access_token={access_token}'.format(user_name=user_name, access_token=session['access_token'])
    response = requests.get(url)
    return jsonify(data=response.text)


@views.route('/get_tags_search')
def get_tags_search():
    # tags = request.args.get('tags')
    tags = 'wilson'
    url = 'https://api.instagram.com/v1/tags/search?q={tags}&access_token={access_token}'.format(tags = tags, access_token=session['access_token'])
    response = requests.get(url)
    return jsonify(data=response.text)

@views.route('/get_user_photos')
def get_user_photos():
    if 'access_token' in session and 'user' in session:
        api = InstagramAPI(access_token=session['access_token'])
        recent_media, next = api.user_recent_media(user_id=session['user'].get('id'), count=5)

        templateData = {
            'size':request.args.get('size', 'thumb'),
            'media':recent_media
        }

        return render_template('media.html', **templateData)
    else:
        return redirect(url_for('account.login'))


@views.route('/download_photos')
def downloads_photos():
    photos = []
    count = request.args.get('count', None)
    max_id = request.args.get('max_id', None)
    api = InstagramAPI(access_token=session['access_token'])
    if max_id is not None:
        user_media, next = api.user_recent_media(count=100, max_id=max_id)
    else:
        user_media, next = api.user_recent_media(count=100)
    for media in user_media:
        # print media.images
        # urllib.urlretrieve(media.images['standard_resolution'].url, '%s.jpg' % media.id)
        photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
        if len(user_media) == 0:
            break
    max_id = user_media[-1].id
    return 'Retrieved %d photos<br/>' % len(photos) + ''.join(photos)
