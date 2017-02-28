import requests, geocoder
from test_app import constants

class RetrieveInstagramData:
    def get_data_from_url(self, url):
        r = requests.get(url)
        json = r.json()
        data = json['data']
        return data

    """Gets all photos for the current user and returns collection as 
    data in returned object"""
    def get_current_user_photos(self, request):
        url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
        url += request.session[constants.ACCESS_TOKEN]
        data = self.get_data_from_url(url)
        context = {
        'images': data
        }
        return context

    """Gets collection of photos by location name"""
    def get_photos(self, request, name, location_id):
        url = 'https://api.instagram.com/v1/locations/' + location_id
        url += '/media/recent?access_token=' + request.session[constants.ACCESS_TOKEN]
        data = self.get_data_from_url(url) 
        context = {
            'images': data,
            'destination': name
        }
        return context

    def get_destination_list(self, request, destination_name):
        #get lat/lon based on name, then use this to feed into instagram API call
        g = geocoder.google(destination_name)
        url = 'https://api.instagram.com/v1/locations/search?lat='
        url += str(g.lat) + '&lng=' + str(g.lng) +'&access_token=' + request.session[constants.ACCESS_TOKEN]
        data = self.get_data_from_url(url)
        context = {
            'destination_list': data
        }
        return context