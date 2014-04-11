#! /usr/bin/env python

# External Imports
import requests
import urllib
import zipfile
from flask import Blueprint, request, redirect, jsonify, render_template, url_for, session, send_file, make_response
from instagram.client import InstagramAPI
from io import BytesIO
from account import instagram_login_required
import json

MAX_COUNT=30

views = Blueprint('views', __name__)

@views.route('/media_by_hashtag')
@instagram_login_required
def media_by_hashtag():
    hashtag = request.args.get('hashtag', 'gamer')
    url = 'https://api.instagram.com/v1/tags/{hashtag}/media/recent?access_token={access_token}'.format(hashtag = hashtag, access_token=session['access_token'])
    response = requests.get(url)
    return jsonify(data=json.loads(response.text))

@views.route('/followed_by')
@instagram_login_required
def followed_by():
    url = 'https://api.instagram.com/v1/users/3/followed-by?access_token={access_token}'.format(access_token=session['access_token'])
    response = requests.get(url)
    return jsonify(data=json.loads(response.text))

@views.route('/get_user_info')
@instagram_login_required
def get_instagram_user_info():
    username=request.args.get('username', 'bunnymama')

    url = 'https://api.instagram.com/v1/users/search?q={username}&count=1&access_token={access_token}'.format(username=username, access_token=session['access_token'])
    response = requests.get(url)
    data = json.loads(response.text)

    templateData = {
        'username':username,
        'user_id': data['data'][0]['id'],
        'full_name':data['data'][0]['full_name'],
        'profile_picture':data['data'][0]['profile_picture'],
        'bio':data['data'][0]['bio']
    }
    return render_template('user.html', **templateData)


@views.route('/get_user_photos')
@instagram_login_required
def get_user_photos():
    count = request.args.get('count', MAX_COUNT)
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.user_recent_media(user_id=session['user'].get('id'), count=count)

    templateData = {
        'size':request.args.get('size', 'thumb'),
        'media':recent_media
    }

    return render_template('media.html', **templateData)

@views.route('/search_by_hashtag')
@instagram_login_required
def search_by_hashtag():
    hashtag = request.args.get('hashtag', 'gamer')
    count = request.args.get('count', MAX_COUNT)
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.tag_recent_media(count, 0, hashtag)
    templateData = {
        'size':request.args.get('size', 'thumb'),
        'media':recent_media
    }
    return render_template('media.html', **templateData)

@views.route('/user_media_feed')
@instagram_login_required
def get_user_media_feed():
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.user_media_feed()

    templateData = {
        'size':request.args.get('size', 'thumb'),
        'media':recent_media
    }

    return render_template('media.html', **templateData)


@views.route('/download_photos')
@instagram_login_required
def downloads_photos():
    # Open StringIO to grab in memory ZIP contents
    zip_mem = BytesIO()
    zipFile = zipfile.ZipFile(zip_mem, 'w')

    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.user_recent_media()

    for media in recent_media:
        f_name = media.images['standard_resolution'].url.rsplit('/', 1)[1]
        r = requests.get(media.images['standard_resolution'].url, stream=True)
        if r.status_code == 200:
            with BytesIO() as img_mem:
                for chunk in r.iter_content(1024 * 10):
                    img_mem.write(chunk)
                print "Adding:", f_name
                zipFile.writestr(f_name, img_mem.getvalue())

    zipFile.close()
    zip_mem.seek(0)

    return send_file(zip_mem,
                     mimetype="application/zip",
                     attachment_filename="instagram.zip",
                     as_attachment=True)
