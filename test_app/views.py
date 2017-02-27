from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import os, requests

client_id = '6e89b63d0f1444faadfdd9f4d198a989'
client_secret = '279299f3b9d745fca8b7261a64289c8f'
access_token = None

REDIRECT_URI = 'redirect_uri'
ACCESS_TOKEN = 'access_token'

"""Sets the redirect URL after being authorized if necessary"""
def set_redirect_uri(request):
    path = request.path
    host = request.META['HTTP_HOST']
    request.session[REDIRECT_URI] = request.scheme + '://' + str(host) + str(path)

"""Sets access_token which is used when requesting data from the API"""
def set_access_token(request):
    code = request.GET.get('code')

    if REDIRECT_URI not in request.session:
        set_redirect_uri(request)

    post_fields = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': request.session[REDIRECT_URI],
        'code': code
    }
    url = 'https://api.instagram.com/oauth/access_token'
    r = requests.post(url, data=post_fields)
    json = r.json()
    request.session[ACCESS_TOKEN] = json['access_token']

def get_current_user_photos(request):
    url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
    url += request.session[ACCESS_TOKEN]
    r = requests.get(url)
    json = r.json()
    data = json['data']
    context = {
    'data': data
    }
    return context

# Create your views here.
def home(request):
    uri = os.path.join(request.build_absolute_uri(), 'authorized/')
    request.session[REDIRECT_URI] = uri
    url = 'https://api.instagram.com/oauth/authorize/?client_id='
    url += client_id + '&redirect_uri=' + uri + '&response_type=code'
    return HttpResponseRedirect(url)

def authorized(request):
    if ACCESS_TOKEN not in request.session:
        set_access_token(request)

    context = get_current_user_photos(request)
    return render(request, 'test_app/authorized.html', context)