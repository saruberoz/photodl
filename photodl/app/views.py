#! /usr/bin/env python

# External Imports
import requests
import urllib
import zipfile
import StringIO
from flask import Blueprint, request, redirect, jsonify, render_template, url_for, session, send_file, make_response
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
    count = request.args.get('count', 100)
    if 'access_token' in session and 'user' in session:
        api = InstagramAPI(access_token=session['access_token'])
        recent_media, next = api.user_recent_media(user_id=session['user'].get('id'), count=count)

        templateData = {
            'size':request.args.get('size', 'thumb'),
            'media':recent_media
        }

        return render_template('media.html', **templateData)
    else:
        return redirect(url_for('account.login'))


@views.route('/download_photos')
def downloads_photos():
    # Open StringIO to grab in memory ZIP contents
    f = StringIO.StringIO()
    zipFile = zipfile.ZipFile(f, 'w')

    photos = []
    count = request.args.get('count', 2) # for now lets do 2 file
    max_id = request.args.get('max_id', None)
    api = InstagramAPI(access_token=session['access_token'])
    if max_id is not None:
        user_media, next = api.user_recent_media(count=count, max_id=max_id)
    else:
        user_media, next = api.user_recent_media(count=count)

    for media in user_media:
        # print media.images
        # result = urllib.urlretrieve(media.images['standard_resolution'].url, '%s.jpg' % media.id)
        result = urllib.urlopen(media.images['standard_resolution'].url)
        print media.images['standard_resolution'].url
        print result
        # print type(result)
        # print dir(result)
        # print result[0]
        # data = requests.get(media.images['standard_resolution'].url)

        zipFile.writestr('%s.jpg' % media.id, result.read())
        # return send_file(result.read(), mimetype="image.jpg", as_attachment=True, attachment_filename='%s.jpg' % media.id)
        # photos.append(urllib.urlretrieve(media.images['standard_resolution'].url, '%s.jpg' % media.id))
        # photos.append('<img src="%s"/>' % media.images['thumbnail'].url)

        if len(user_media) == 0:
            break
    # zipFile.close()

    max_id = user_media[-1].id
    return send_file(zipFile,
                     mimetype="application/zip",
                     attachment_filename="instagram.zip",
                     as_attachment=True)
    # import HttpResponse
    # response = HttpResponse(f.getValue(), content_type="application/zip")
    # response['Content-Disposition'] = "attachment; filename=instagram.zip"
    # response = make_response(zipFile)
    # response.headers['Content-Disposition'] = "attachment"; filename="instagram.zip"
    # return 'Retrieved %d photos<br/>' % len(photos) + ''.join(photos)
