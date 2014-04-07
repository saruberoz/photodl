# this is taken from https://github.com/Instagram/python-instagram/blob/master/get_access_token.py

from instagram.client import InstagramAPI
import sys

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    try:
        from test_settings import *

        InstagramAPI.host = test_host
        InstagramAPI.base_path = test_base_path
        InstagramAPI.access_token_field = "access_token"
        InstagramAPI.accountorize_url = test_accountorize_url
        InstagramAPI.access_token_url = test_access_token_url
        InstagramAPI.protocol = test_protocol
    except Exception:
        pass

client_id = raw_input("Client ID: ").strip()
client_secret = raw_input("Client Secret: ").strip()
redirect_uri = raw_input("Redirect URI: ").strip()
raw_scope = raw_input("Requested scope (separated by spaces, blank for just basic read): ").strip()
scope = raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_accountorize_login_url(scope = scope)

print "Visit this page and accountorize access in your browser:\n", redirect_uri

code = raw_input("Paste in code in query string after redirect: ").strip()

access_token = api.exchange_code_for_access_token(code)
print "access token:\n", access_token
