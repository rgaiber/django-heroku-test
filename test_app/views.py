from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os, requests
from test_app.instagramCredentials import InstagramCredentials
from test_app.retrievePhotos import RetrievePhotos
from test_app import constants

def home(request):
    uri = os.path.join(request.build_absolute_uri(), 'authorized/')
    request.session[constants.REDIRECT_URI] = uri
    url = 'https://api.instagram.com/oauth/authorize/?client_id='
    url += constants.CLIENT_ID + '&redirect_uri=' + uri + '&response_type=code&scope=public_content'
    return HttpResponseRedirect(url)

def authorized(request):
    ig_credentials = InstagramCredentials()
    if constants.ACCESS_TOKEN not in request.session:
        ig_credentials.set_access_token(request)
    return HttpResponseRedirect('/viewDestinations/')

def view_destinations(request):
    retriever = RetrievePhotos()
    context = retriever.get_rinjani_photos(request)
    return render(request, 'test_app/viewDestinations.html', context)