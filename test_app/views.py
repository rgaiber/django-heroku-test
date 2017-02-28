from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import os, requests

CLIENT_ID = '6e89b63d0f1444faadfdd9f4d198a989'
CLIENT_SECRET = '279299f3b9d745fca8b7261a64289c8f'
REDIRECT_URI = 'redirect_uri'
ACCESS_TOKEN = 'access_token'

"""Sets the redirect URI based on current URI"""
def set_redirect_uri(request):
    path = request.path
    host = request.META['HTTP_HOST']
    request.session[REDIRECT_URI] = request.scheme + '://' + str(host) + str(path)

"""Sets the access token and stores it to session"""
def set_access_token(request):
    code = request.GET.get('code')

    if REDIRECT_URI not in request.session:
        set_redirect_uri(request)

    post_fields = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': request.session[REDIRECT_URI],
        'code': code
    }
    url = 'https://api.instagram.com/oauth/access_token'
    r = requests.post(url, data=post_fields)
    json = r.json()
    request.session[ACCESS_TOKEN] = json['access_token']

"""Gets all photos for the current user and returns collection as 
data in returned object"""
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

"""Gets recent photos tagged in Gunung Rinjani National Park"""
def get_rinjani_photos(request):
    location_id = '886917800'
    url = 'https://api.instagram.com/v1/locations/' + location_id
    url += '/media/recent?access_token=' + request.session[ACCESS_TOKEN]
    r = requests.get(url)
    json = r.json()
    data = json['data']
    context = {
        'data': data,
        'destination': 'Torres Del Paine'
    }
    return context

# Create your views here.
def home(request):
    uri = os.path.join(request.build_absolute_uri(), 'authorized/')
    request.session[REDIRECT_URI] = uri
    url = 'https://api.instagram.com/oauth/authorize/?client_id='
    url += CLIENT_ID + '&redirect_uri=' + uri + '&response_type=code&scope=public_content'
    return HttpResponseRedirect(url)

def authorized(request):
    if ACCESS_TOKEN not in request.session:
        set_access_token(request)
    return HttpResponseRedirect('/viewDestinations/')

def view_destinations(request):
    context = get_rinjani_photos(request)
    return render(request, 'test_app/viewDestinations.html', context)