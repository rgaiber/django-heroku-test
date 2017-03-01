from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os, requests
from test_app.instagramCredentials import InstagramCredentials
from test_app.retrieveInstagramData import RetrieveInstagramData
from test_app import constants
from test_app.forms import DestinationSelectionForm

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
    retriever = RetrieveInstagramData()
    context = {}
    # if the user entered text, populate the dropdown with completed destination options
    # for them to select from
    if request.method == constants.GET:
        form = DestinationSelectionForm(request.GET)
        if form.is_valid():
            context = retriever.get_destination_list(request, form.cleaned_data['destination_name'])
    else:
        form = DestinationSelectionForm()
    context['form'] = form

    return render(request, 'test_app/viewDestinations.html', context)

def view_photos(request, destination_id, destination_name):
    retriever = RetrieveInstagramData()
    context = retriever.get_photos(request, destination_name, destination_id)
    form = DestinationSelectionForm(request.GET)
    context['form'] = form

    return render(request, 'test_app/viewDestinations.html', context)
