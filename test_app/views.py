from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import os, requests

client_id = '6e89b63d0f1444faadfdd9f4d198a989'
client_secret = '279299f3b9d745fca8b7261a64289c8f'
redirect_uri = None
access_token = None

"""Sets the redirect URL after being authorized if necessary"""
def set_redirect_url(request):
    global redirect_uri
    path = request.path
    host = request.META['HTTP_HOST']
    redirect_uri = request.scheme + '://' + str(host) + str(path)

"""Sets access_token which is used when requesting data from the API"""
def set_access_token(request):
    code = request.GET.get('code')
    global redirect_uri
    global access_token

    if redirect_uri == None:
        set_redirect_url(request)

    post_fields = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    url = 'https://api.instagram.com/oauth/access_token'
    r = requests.post(url, data=post_fields)
    json = r.json()
    access_token = json['access_token']

def get_current_user_photos():
    url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
    url += access_token
    r = requests.get(url)
    json = r.json()
    data = json['data']
    context = {
    'data': data
    }
    return context

# Create your views here.
def home(request):
    global redirect_uri
    redirect_uri = os.path.join(request.build_absolute_uri(), 'authorized/')
    url = 'https://api.instagram.com/oauth/authorize/?client_id='
    url += client_id + '&redirect_uri=' + redirect_uri + '&response_type=code'
    return HttpResponseRedirect(url)

def authorized(request):
    global access_token
    if access_token == None:
        set_access_token(request)

    context = get_current_user_photos()
    return render(request, 'test_app/authorized.html', context)