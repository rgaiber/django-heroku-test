import requests
from test_app import constants

class RetrievePhotos:
    """Gets all photos for the current user and returns collection as 
    data in returned object"""
    def get_current_user_photos(self, request):
        url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
        url += request.session[constants.ACCESS_TOKEN]
        r = requests.get(url)
        json = r.json()
        data = json['data']
        context = {
        'data': data
        }
        return context

    """Gets recent photos tagged in Gunung Rinjani National Park"""
    def get_rinjani_photos(self, request):
        location_id = '886917800'
        url = 'https://api.instagram.com/v1/locations/' + location_id
        url += '/media/recent?access_token=' + request.session[constants.ACCESS_TOKEN]
        r = requests.get(url)
        json = r.json()
        data = json['data']
        context = {
            'data': data,
            'destination': 'Torres Del Paine'
        }
        return context