import requests

from test_app import constants

class InstagramCredentials:
    """Sets the redirect URI based on current URI"""
    def set_redirect_uri(self, request):
        path = request.path
        host = request.META['HTTP_HOST']
        request.session[constants.REDIRECT_URI] = request.scheme + '://' + str(host) + str(path)

    """Sets the access token and stores it to session"""
    def set_access_token(self, request):
        code = request.GET.get('code')

        if constants.REDIRECT_URI not in request.session:
            set_redirect_uri(request)

        post_fields = {
            'client_id': constants.CLIENT_ID,
            'client_secret': constants.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': request.session[constants.REDIRECT_URI],
            'code': code
        }
        url = 'https://api.instagram.com/oauth/access_token'
        r = requests.post(url, data=post_fields)
        json = r.json()
        request.session[constants.ACCESS_TOKEN] = json['access_token']