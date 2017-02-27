from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from instagram.client import InstagramAPI


import os, requests

#https://api.instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=code
client_id = '6e89b63d0f1444faadfdd9f4d198a989'
client_secret = '279299f3b9d745fca8b7261a64289c8f'

# Create your views here.
def home(request):
    redirect_uri = os.path.join(request.build_absolute_uri(), 'authorized/')
    url = 'https://api.instagram.com/oauth/authorize/?client_id='
    url += client_id + '&redirect_uri=' + redirect_uri + '&response_type=code'
    return HttpResponseRedirect(url)

def authorized(request):
    code = request.GET.get('code')

    #TODO: do this in better way, seems hacky
    path = request.path
    host = request.META['HTTP_HOST']
    redirect_uri = request.scheme + '://' + str(host) + str(path)

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
    return HttpResponse('Access token:' + access_token)