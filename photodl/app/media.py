#! /usr/bin/env python

# External Imports
from datetime import datetime
import requests
import zipfile
from flask import Blueprint, request, render_template, session, send_file
from io import BytesIO
from instagram.client import InstagramAPI

# Internal Imports
from account import instagram_login_required

MAX_COUNT = 30
MAX_ID = 0

media = Blueprint('media', __name__)


@media.route('/most_popular')
@instagram_login_required
def get_most_popular():
    count = request.args.get('count', MAX_COUNT)
    max_id = request.args.get('max_id', MAX_ID)

    api = InstagramAPI(access_token=session['access_token'])
    recent_media = api.media_popular(count, max_id)

    templateData = {
        'size': request.args.get('size', 'thumb'),
        'media': recent_media
    }

    return render_template('media.html', **templateData)


@media.route('/get_user_photos')
@instagram_login_required
def get_user_photos():
    count = request.args.get('count', MAX_COUNT)
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = \
        api.user_recent_media(user_id=session['user'].get('id'), count=count)

    templateData = {
        'size': request.args.get('size', 'thumb'),
        'media': recent_media
    }

    return render_template('media.html', **templateData)


@media.route('/search_by_hashtag')
@instagram_login_required
def search_by_hashtag():
    hashtag = request.args.get('hashtag', 'gamer')
    count = request.args.get('count', MAX_COUNT)
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.tag_recent_media(count, MAX_ID, hashtag)
    templateData = {
        'size': request.args.get('size', 'thumb'),
        'media': recent_media
    }
    return render_template('media.html', **templateData)


@media.route('/user_media_feed')
@instagram_login_required
def get_user_media_feed():
    api = InstagramAPI(access_token=session['access_token'])
    recent_media, next = api.user_media_feed()

    templateData = {
        'size': request.args.get('size', 'thumb'),
        'media': recent_media
    }

    return render_template('media.html', **templateData)


@media.route('/download_photos')
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

    download_fname = datetime.today().strftime("%Y-%m-%d")
    return send_file(zip_mem,
                     mimetype="application/zip",
                     attachment_filename="photodl-%s.zip" % download_fname,
                     as_attachment=True)
