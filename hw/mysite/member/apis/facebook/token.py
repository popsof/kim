from django.conf import settings
import requests
import json

__all__ = [
    'get_access_token',
    'get_user_id_from_token',
    'debug_token',
    'get_user_info',
]

app_id = settings.FACEBOOK_APP_ID
secret_code = settings.FACEBOOK_SECRET_CODE

app_access_token = '{}|{}'.format(app_id, secret_code)


def get_access_token(code, redirect_uri):
    
    url_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token' \
                        '?client_id={}' \
                        '&redirect_uri={}' \
                        '&client_secret={}' \
                        '&code={}'.format(
                        app_id, redirect_uri, secret_code, code)

    r = requests.get(url_access_token)
    rsp_access_token = r.json()
    return rsp_access_token.get('access_token')


def get_user_id_from_token(access_token):
    rsp_debug_token = debug_token(access_token)
    print(rsp_debug_token)
    return rsp_debug_token['data']['user_id']


def debug_token(access_token):
    url_debug_token = 'https://graph.facebook.com/debug_token' \
                        '?input_token={}' \
                        '&access_token={}'.format(
                        access_token, app_access_token)
                                    
    print(url_debug_token)
    r = requests.get(url_debug_token)
    rsp_debug_token = r.json()
    return rsp_debug_token


def get_user_info(user_id, access_token):
    url_user_info = 'https://graph.facebook.com/{}' \
                    '?access_token={}' \
                    '&fields=id,first_name,last_name,gender,picture,email'.format(
                    user_id, access_token)

    r = requests.get(url_user_info)
    rsp_user_info = r.json()
    return rsp_user_info

